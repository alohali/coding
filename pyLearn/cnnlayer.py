from enum import Enum
import numpy as np

class Type(Enum):
    """Layer type"""
    FC = 1,
    CONV = 2,
    POOL = 3,
    LRN = 4,
    DATA = 5,
    ELEM_WISE = 6,
    OTHER = 7


class Layer(object):
    """Single layer of CNN that contains split info"""
    def __init__(self, data_size):
        self.data_size = data_size
        self.pad = 0
        self.uv = self.rs = 1
        self.split = False
        self.recombine = False
        self.w_divide = self.h_divide = 1
        self.halo = np.zeros(4, dtype=int) #left, right, up, down
        self.module_size = 1 #for inception modules

        
    def setParam(self,**kwargs):
        self.name = kwargs['name']
        self.type = kwargs['type']
        self.nchwkpq = kwargs['nchwkpq']
        self.pre = kwargs['pre']
        self.suc = kwargs['suc']
        if self.type in [Type.CONV, Type.POOL]:
            self.rs, self.uv = kwargs['rsuv']
            self.pad = kwargs['pad']

        self.weight_size = self.__weight_size()
        self.output_size = self.__output_size()
        self.input_size  = self.__input_size()
        if self.is_winograd:
            # add winograd weights into consideration as low L2 hitrate
            self.memory_footprint = self.input_size + self.output_size + self.weight_size  
        else:
            self.memory_footprint = self.input_size + self.output_size 


    def __output_size(self):
        return self.nchwkpq[0] * self.nchwkpq[4] * self.nchwkpq[5] * self.nchwkpq[6] * self.data_size #nkpq

    def __input_size(self):
        return self.nchwkpq[0] * self.nchwkpq[1] * self.nchwkpq[2] * self.nchwkpq[3] * self.data_size #nchw

    def is_winograd(self):
        """ only 3x3 conv and c*k>>c+k should use winograd now """
        if (self.type == Type.CONV and self.rs == 3):  
            if (self.nchwkpq[1] > 3):
                return True
        return False

    def __weight_size(self):
        """ calc weight. 3x3 winograd should be 16/9 conv weight"""
        w = 0
        if (self.type == Type.CONV):
            w = self.rs * self.rs * self.nchwkpq[1] * self.nchwkpq[4] * self.data_size
            if self.is_winograd():  # + weight size for winograd
                w = w * 16 / 9
        if (self.type == Type.FC):
            w = reduce(lambda x, y: x * y, self.nchwkpq[1:]) * self.data_size
        return w

    def calc_halo(self, halo_last):
        """halo calc"""
        #halo = halo_last[:]
        #left = old * uv + pad, right = old * uv + rs -1 -pad -uv/2
        #halo *= layer.uv
        if self.w_divide>1:
            left = self.pad
            right = self.rs - 1 - self.pad - self.uv/2
        else:
            left = right = 0
        if self.h_divide>1:
            up = self.pad
            down = self.rs - 1 - self.pad - self.uv/2
        else:
            up = down = 0
        self.halo = halo_last * self.uv + [left, right, up, down]
        #print self.halo


    def halo_percent(self,halo):
        hori_halo = (halo[0]+halo[1]) * self.nchwkpq[2]
        vert_halo = (halo[2]+halo[3]) * self.nchwkpq[3]
        area      = self.nchwkpq[2] * self.nchwkpq[3]
        total = hori_halo * (self.w_divide-1) + vert_halo * (self.h_divide - 1)
        return float(total) / float(area)


