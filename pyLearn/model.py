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


class Layer(object):
    """Single layer of CNN that contains split info"""
    data_size = 1

    def __init__(self):
        self.split = False
        self.recombine = False
        self.w_divide = self.h_divide = 1
        self.halo = np.zeros(4, dtype=int) #left, right, up, down

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

    def calc_halo(self, halo_last, layer):
        """halo calc"""
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
        return float(total) / float(area)

class Network(object):
    """Network init, build and sort"""
    def __init__(self):
        self.layer_map = dict() #string to layer
        self.root   = None
        self.sorted = False
        self.sorted_layers = list()

    def insert_layer(self, **kwargs):
        layer = Layer()
        layer.setParam(**kwargs)
        if not layer.name in self.layer_map:
            self.layer_map[layer.name] = layer
        else:
            raise ValueError,"duplicate layer!"


    def sort_net(self):
        if self.root==None:
            raise ValueError,"No root of net!"
        #I don't know if dfs is better or dfs
        self.sorted = True
        self.__toposort("dfs") 

    def __toposort(self, type):
        if type=="dfs":
            list0 = Queue.LifoQueue() #stack
        elif type=="bfs":
            list0 = Queue.Queue() #queue
        #traverse
        list0.put(self.root)
        while not list0.empty():
            layer = list0.get()
            self.sorted_layers.append(layer)
            layer = self.layer_map[layer]

            for suc in layer.suc:
                real_suc = self.layer_map[suc]
                indegree = len(real_suc.pre)
                for pre in real_suc.pre:
                    if pre in self.sorted_layers:
                        indegree -= 1
                if indegree==0:
                    list0.put(suc)
        print "sorted_layers,", self.sorted_layers

    def __lifetime(self):
        assert 0,"Haven't implemented"

class Surrond0831(Network):
    """network surrond0831"""
    def __init__(self):
        super(Surrond0831, self).__init__()
        self.root = "data0"
        args = {'name':"data0", 'type':Type.DATA, 'nchwkpq':[1, 3 , 544, 960, 3 , 544, 960],\
                'pre':[], 'suc':['conv0']}
        self.insert_layer(**args)
        args = {'name':"conv0", 'type':Type.CONV, 'nchwkpq':[1, 3 , 544, 960, 16, 272, 480],\
                'pre':["data0"], 'suc':['conv1'],'rsuv':[7, 2], 'pad':3}
        self.insert_layer(**args)
        args = {'name':"conv1", 'type':Type.CONV, 'nchwkpq':[1, 16, 272, 480, 56, 136, 240],\
                'pre':["conv0"], 'suc':['conv2'],'rsuv':[3, 2], 'pad':1}
        self.insert_layer(**args)
        args = {'name':"conv2", 'type':Type.CONV, 'nchwkpq':[1, 56, 136, 240, 64, 136, 240],\
                'pre':["conv1"], 'suc':['conv3'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)
        args = {'name':"conv3", 'type':Type.CONV, 'nchwkpq':[1, 64, 136, 240, 64, 136, 240],\
                'pre':["conv2"], 'suc':['conv4'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)
        args = {'name':"conv4", 'type':Type.CONV, 'nchwkpq':[1, 64, 136, 240, 64, 136, 240],\
                'pre':["conv3"], 'suc':['conv5'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)
        args = {'name':"conv5", 'type':Type.CONV, 'nchwkpq':[1, 64, 136, 240,104, 68 , 120],\
                'pre':["conv4"], 'suc':['conv6'],'rsuv':[3, 2], 'pad':1}
        self.insert_layer(**args)
        args = {'name':"conv6", 'type':Type.CONV, 'nchwkpq':[1,104, 68 , 120,112, 68 , 120],\
                'pre':["conv5"], 'suc':[       ],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)

        self.sort_net()


class SplitNet(object):
    """ SPLIT STRATEGY DESIGN"""
    max_split_layers = 5
    max_halo_persent = 0.1
    def __init__(self, L3size, net):
        self.L3size_ = L3size
        self.split_layers_cnt = 0
        self.network = net


    def split_net(self):
        """traverse each layer and calculate split"""
        for i in self.network.sorted_layers:
            layer = self.network.layer_map[i]
            if layer.type == Type.DATA:
                continue
            layer.h_divide, layer.w_divide = self.__cacl_split(layer)
            self.split_layers_cnt = self.__split_cnt_calc(layer)
            layer.recombine = self.__recombine(layer)
            if layer.split:
                print "split,%s,h,%d,w,%d" % (layer.name, layer.h_divide, layer.w_divide)
            if layer.recombine:
                print "Recombine at layer: %s" % layer.name

    def __calc_divide(self, layer):
        assert 0



    def __cacl_split(self, layer):
        """
            not split when:
            1, suc > 1
            2, memory foot print < L3size
        """
        if len(layer.suc) > 1 or layer.memory_footprint < self.L3size_:
            ret = [1,1]
        else:
            io_size = layer.input_size + layer.output_size #- layer.weight_size
            cache   = self.L3size_ #- layer.weight_size, not consider weights now
            if layer.is_winograd():
                cache -= layer.weight_size
            
            if   io_size/2 < cache:
                ret = [1,2]
            elif io_size/3 < cache:
                ret = [1,3]
            elif io_size/4 < cache:
                ret = [1,4]
            elif io_size/6 < cache:
                ret = [2,3]
            elif io_size/8 < cache:
                ret = [2,4]
            else:
                print "too big memory!!!!!!! not implemented now...@_@#", layer.name, layer.memory_footprint
                ret = [1,1]

        pre_layer = self.network.layer_map[layer.pre[0]]
        if pre_layer.split and not pre_layer.recombine: #same as last layer if not recombine
            if ret[0]*ret[1]==1:
                self.__recombie_last_layer(pre_layer)
            elif pre_layer.h_divide * pre_layer.w_divide < ret[0]*ret[1]: 
                self.__recombie_last_layer(pre_layer)
            elif pre_layer.h_divide * pre_layer.w_divide > ret[0]*ret[1]:
                ret = [pre_layer.h_divide, pre_layer.w_divide]

        if ret[0]*ret[1]==1:
            layer.split = False
        else:
            layer.split = True
        return ret



    def __split_cnt_calc(self, layer):
        """ cnt chained split   """
        pre_layer = self.network.layer_map[layer.pre[0]]
        if pre_layer.split and not pre_layer.recombine:
            return self.split_layers_cnt + 1
        elif layer.split:
            return 1
        else:
            return 0

    def __recombine(self, layer):
        """
            recombine when:
            1, successor number =0 or >1
            1, successor has multi input
            2, halo > 10%
            3, split layers > 5
            4, total memory of successor < L3 size
            5, successor h_divide * w_divide > current h_divide * w_divide
            4,5 calc in next layer's split
        """
        if not layer.split:
            print "~~~~~~~~"
            return False
        elif len(layer.suc)==0:
            return True
        elif len(layer.suc)>1:
            print "multi output"
            return True
        elif len(self.network.layer_map[layer.suc[0]].pre)>1:
            print "next layer multi input"
            return True
        elif self.split_layers_cnt > self.max_split_layers:
            print "chained cnt,", self.max_split_layers
            return True
        elif 0 > self.max_halo_persent:#need to do 
            print "halo percent,", 0 
            return True

    def __recombie_last_layer(self, last_layer):
        print "last layer recombine"
        last_layer.recombine = True



if __name__ == '__main__':
    net0 = Surrond0831()

    splitTest = SplitNet(4096 * 1024, net0)

    if net0.sorted:
        splitTest.split_net()


