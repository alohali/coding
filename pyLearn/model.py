#!/usr/bin/env python
import Queue
import numpy as np
from enum import Enum


class Type(Enum):
    """Layer type"""
    FC = 1,
    CONV = 2,
    POOL = 3,
    NORM = 4,
    DATA = 5,
    ELEM_WISE = 6,
    OTHER = 7


class Layer:
    """Single layer of CNN that contains split info"""
    data_size = 1

    def __init__(self):
        self.split = False
        self.recombine = False
        self.w_divide = self.h_divide = 1
        self.halo = np.zeros(4, dtype=int) #left, right, up, down

    def setParam(self,**kw):
        self.name = kw['name']
        self.type = kw['type']
        self.nchwkpq = kw['nchwkpq']
        self.pre = kw['pre']
        self.suc = kw['suc']
        if self.type in [Type.CONV, Type.POOL]:
            self.rs, self.uv = kw['rsuv']
            self.pad = kw['pad']
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
        size = 0
        for pre in self.pre:
            size += pre.output_size
        return size

    def is_winograd(self):
        if (self.type == Type.CONV and self.rs == 3):  # only 3x3 winograd now
            if (self.nchwkpq[1] > 3):#c>3
                return True
        return False

    def __weight_size(self):
        w = 0
        if (self.type == Type.CONV):
            w = self.rs * self.rs * self.nchwkpq[1] * self.nchwkpq[4] * self.data_size
            if self.is_winograd():  # + weight size for winograd
                w = w * 16 / 9
        if (self.type == Type.FC):
            w = reduce(lambda x, y: x * y, self.nchwkpq[1:]) * self.data_size
        return w

    def __calc_halo(self, halo_last, layer):
        halo = halo_last[:]
        #left = old * uv + pad, right = old * uv + rs -1 -pad -uv/2
        halo *= layer.uv
        left_up = layer.pad
        right_down = rs - 1 - pad - uv/2  
        return halo + [left_up, right_down, left_up, right_down]


    def halo_percent(self,halo):
        hori_halo = (halo[0]+halo[1]) * nchwkpq[2]
        vert_halo = (halo[2]+halo[3]) * nchwkpq[3]
        area      = nchwkpq[2] * nchwkpq[3]
        total = hori_halo * (self.w_divide-1) + vert_halo * (self.h_divide - 1)
        return float(halo) / float(area)




class SplitNet:
    """ SPLIT STRATEGY DESIGN"""
    max_split_layers = 5
    max_halo_persent = 0.1
    def __init__(self, L3size):
        self.L3size_ = L3size
        self.split_layers_cnt = 0

    def split(self, sorted_layers):
        """split each layer"""
        for layer in sorted_layers:
            if layer.type == Type.DATA:
                continue
            layer.split = self.__need_split(layer)
            self.split_layers_cnt = self.__split_cnt_calc(layer)
            layer.h_divide, layer.w_divide = self.__calc_divide(layer)
            layer.recombine = self.__recombine(layer)
            print "split,%s,h,%d,w,%d" % (layer.name, layer.h_divide, layer.w_divide)
            if layer.recombine:
                print "Recombine at layer: %s" % layer.name

    def __calc_divide(self, layer):
        if not layer.split:
            return [1,1]
        if layer.pre[0].split and not layer.pre[0].recombine: #same as last layer if not recombine
            return [layer.pre[0].h_divide, layer.pre[0].w_divide]

        io_size = layer.input_size + layer.output_size #- layer.weight_size
        cache   = self.L3size_ #- layer.weight_size, not consider weights now
        if layer.is_winograd():
            cache -= layer.weight_size
        if   io_size/2 < cache:
            return [1,2]
        elif io_size/3 < cache:
            return [1,3]
        elif io_size/4 < cache:
            return [1,4]
        elif io_size/6 < cache:
            return [2,3]
        elif io_size/8 < cache:
            return [2,4]
        else:
            print "too big memory!!!!!!! not implemented now...@_@#", layer.name, layer.memory_footprint
            return [1,1]



    def __need_split(self, layer):
        ret = False
        if layer.pre[0].split and not layer.pre[0].recombine: #same as last layer if not recombine
            ret = True
        elif len(layer.suc) > 1:
            pass
        elif layer.memory_footprint > self.L3size_:
            ret = True
        return ret

    def __split_cnt_calc(self, layer):
        if layer.pre[0].split and not layer.pre[0].recombine:
            return self.split_layers_cnt + 1
        elif layer.split:
            return 1
        else:
            return 0

    def __recombine(self, layer):
        if not layer.split:
            return False
        if len(layer.suc)==0 or len(layer.suc)>1:
            return True
        elif self.split_layers_cnt > self.max_split_layers:
            return False
        elif layer.halo_percent > self.max_halo_persent:
            return False
        elif layer.suc[0].memory_footprint < self.L3size_:
            return True
            

class Network:
    """Network init, build and sort"""
    def __init__(self):
        self.layers = dict() #string to layer
        self.root   = None
        self.sorted = False
        self.sorted_layers = list()
    
    def insert_layer(self, layer, is_root):
        if not layer.name in self.layers:
            self.layers[layer.name] = layer
        else:
            raise ValueError,"duplicate layer!"

        if is_root:
            if self.root == None:
                self.root = layer
            else:
                raise ValueError,"duplicate root!"

    def build_net(self):
        if self.root==None:
            raise ValueError,"No root no net!"
        self.dfs_toposort(self.root)

    def dfs_toposort(self):
        assert 0,"Haven't implemented"

    def lifetime(self):
        assert 0,"Haven't implemented"

class surrond0831(Network):
    """network surrond0831"""
    def __init__(self):
        super(surrond0831, self).__init__()
        assert 0,"need to do quickly"
        #start from here 1127
if __name__ == '__main__':
    network = surrond0831()
    network.build_net()

    splitTest = SplitNet(4096 * 1024)

    if network.sorted:
        splitTest.split(network.layers)


