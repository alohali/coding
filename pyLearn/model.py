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
        self.halo_total = 0 

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



class SplitNet:
    """ SPLIT STRATEGY DESIGN"""
    def __init__(self, L3size):
        self.L3size_ = L3size

    def split(self, net):
        for layer in net.Layers:
            if layer.type == Type.DATA:
                pass
            layer.split = __need_split(layer)
            layer.h_divide, layer.w_divide = __calc_divide(layer)
            print "split," , layer.name , "w,", layer.h_divide,"h,", layer.w_divide
            layer.recombine = self.__recombine()

    def __calc_divide(self, layer):
        if not layer.split:
            return [1,1]
        if layer.pre[0].split and not layer.pre[0].recombine: #same as last layer if not recombine
            return [layer.pre[0].h_divide, layer.pre[0].w_divide]

        io_size = layer.input_size + layer.output_size #- layer.weight_size
        cache   = self.L3size_ #- layer.weight_size, not consider weights now
        if layer.is_winograd():
            cache -= layer.weight_size
        if io_size < cache/2:
            return [1,2]
        elif io_size < cache/3:
            return [1,3]
        elif io_size < cache/4:
            return [1,4]
        elif io_size < cache/6:
            return [2,3]
        elif io_size < cache/8:
            return [2,4]
        else:
            print "too large memory!!!!!!! not implemented now...@_@#"
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

    def __recombine(self, layer):
        if not layer.split:
            return False
        if len(layer.suc)==0 or len(layer.suc)>1:
            return True
        else:
            

    def calc_halo(self, halo_last, layer):
        halo = halo_last[:]
        #left = old * uv + pad, right = old * uv + rs -1 -pad -uv/2
        halo *= layer.uv
        left_up = layer.pad
        right_down = rs - 1 - pad - uv/2  
        return halo + [left_up, right_down, left_up, right_down]

class Network:
    """Network init and sort"""
    def __init__(self):
        data0 = Layer()
        conv0 = Layer()
        pool0 = Layer()
        conv1 = Layer()
        conv2 = Layer()
        self.root_ = data0
        data0.setParam(name='data0', type=Type.DATA, nchwkpq= [1, 3, 540, 960, 3, 540, 960],pre=[], suc=[conv0])
        conv0.setParam(name='conv0', type=Type.CONV, rsuv=[7, 2], pad=3, nchwkpq= [1, 3, 540, 960, 64, 270, 480]  ,pre=[data0], suc=[pool0])
        pool0.setParam(name='pool0', type=Type.POOL, rsuv=[3, 2], pad=1, nchwkpq= [1, 64, 270, 480, 64, 135, 240] ,pre=[conv0], suc=[conv1])
        conv1.setParam(name='conv1', type=Type.CONV, rsuv=[1, 0], pad=0, nchwkpq= [1, 64, 135, 240, 64, 135, 240] ,pre=[pool0], suc=[conv2])
        conv2.setParam(name='conv2', type=Type.CONV, rsuv=[3, 1], pad=1, nchwkpq= [1, 64, 135, 240, 192, 135, 240],pre=[conv1], suc=[])
        self.Layers = [data0, conv0, pool0, conv1, conv2]  # in dfs+toposort

    def dfs_toposort(self):
        assert 0,"Haven't implemented"

    def lifetime(self):
        assert 0,"Haven't implemented"

if __name__ == '__main__':
    driveNet = Network()
    splitTest = SplitNet(4096 * 1024)
    splitTest.split(driveNet)


