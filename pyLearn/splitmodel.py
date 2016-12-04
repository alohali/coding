#!/usr/bin/env python3
import os
import sys
import subprocess
import re 
import numpy as np

import network
import cnnlayer

class GlobalParam(object):
    """
        define GlobalParam, can lead to different split strategy
    """
    def __init__(self, *args, **kwargs):
        self.data_size = 1
        self.topo_method ="dfs"
        self.max_split_layers = 5
        self.L3size = 4096 * 1024
        self.max_halo_persent = 0.1

        

class SplitNet(object):
    """ SPLIT STRATEGY DESIGN"""
    def __init__(self, g_param, network):
        self.split_layers_cnt = 0
        self.network = network
        self.L3size_ = g_param.L3size
        self.max_halo_persent = g_param.max_halo_persent
        self.max_split_layers = g_param.max_split_layers

    def split_net(self):
        """traverse each layer and calculate split"""
        for i in self.network.sorted_layers:
            layer = self.network.layer_map[i]
            if layer.type == cnnlayer.Type.DATA:
                continue
            layer.h_divide, layer.w_divide = self.__cacl_split(layer)
            self.split_layers_cnt = self.__split_cnt_calc(layer)
            layer.recombine = self.__recombine(layer)

            if self.split_layers_cnt==1 and layer.recombine:
                self.__cancel_split(layer)
            if layer.recombine:
                self.__update_halo(layer)


    def print_result(self):
        for i in self.network.sorted_layers:
            layer = self.network.layer_map[i]
            if layer.split:
                print "split layer, %s,h,%d,w,%d," % (layer.name, layer.h_divide, layer.w_divide), "halo size,", layer.halo
            else:
                print "full  layer, %s" % layer.name
            if layer.recombine:
                print "Recombine  , %s" % layer.name
            if layer.module_size>1:
                print "module_size, %s" % layer.module_size

    def __calc_divide(self, layer):
        assert 0,"not using this"

    def __cancel_split(self, layer):
        """cancel split when needed"""
        layer.split = False
        layer.h_divide = layer.w_divide = 1
        layer.recombine = False

    def __cacl_split(self, layer):
        """
            not split when:
                1, successor number > 1
                2, memory foot print < L3size
            current code:
                split parts = iosize/cache
                h,w = [1,divide  ] when divide < 6
                h,w = [w,divide/2] when divide =6,8
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
                self.__recombie_layer(pre_layer)
            elif pre_layer.h_divide * pre_layer.w_divide < ret[0]*ret[1]: 
                self.__recombie_layer(pre_layer)
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
            2, split layers > 5, recombine into 3+3
            3, halo > 10%, have not implement, needed? 11.29: No, never happen due to (2). 

            implement 4,5 in next layer's split:
            4, total memory of successor < L3 size
            5, successor h_divide * w_divide > current h_divide * w_divide
        """
        if not layer.split:
            return False
        elif len(layer.suc)==0:
            return True
        elif len(layer.suc)>1:
            print "\t[DBG]multi output"
            return True
        elif len(self.network.layer_map[layer.suc[0]].pre)>1:
            print "\t[DBG]next layer multi input"
            return True
        elif self.split_layers_cnt > self.max_split_layers:
            #print "\t[DBG]chained cnt,", self.split_layers_cnt
            self.split_layers_cnt -= self.__recombie_half_of_total(layer)
            return False
            #self.split_layers_cnt -= 3
        #return True
        #elif 0 > self.max_halo_persent:#need to do 
         #   print "\t[DBG]halo percent,", 0 
         #   return True

    def __recombie_last_layer(self, last_layer):
        last_layer.recombine = True
        self.__update_halo(last_layer)

    def __recombie_layer(self, layer):
        layer.recombine = True
        self.__update_halo(layer)


    def __recombie_half_of_total(self, layer):
        """
            choose an old layer to recombine when chained too much layers
            recombine half or at a pooling layer(choose pooling in order to reduce dram)
        """
        cnt = 0
        half_total = (self.max_split_layers + 1)/2
        old_layer = layer
        while cnt<half_total:
            old_layer = self.network.get_layer_by_name(old_layer.pre[0])
            cnt += 1
            if cnt >= 2 and old_layer.type==cnnlayer.Type.POOL:
                break
        self.__recombie_layer(old_layer)
        print half_total, cnt
        print old_layer.name
        return cnt



    def __split_divide(self, layer):
        """
            todo:
            1, when split_layers_cnt>6, divide into 3,3
            2, when halo percent>10% and split_layers_cnt>4, divide into 2+x
        """
        assert 0, "have not implemented, should be faster"


    def __update_halo(self, layer):
        """
            update halo size only when recombine
            update from down to up
        """
        if not layer.recombine:
            return 
        pre_halo = np.zeros(4, dtype=int)
        while layer.split:
            layer.calc_halo(pre_halo)
            pre_halo = layer.halo[:]
            if len(layer.pre)>1:
                raise ValueError, "[DBG]error split"
            layer = self.network.layer_map[layer.pre[0]]
            if layer.recombine:
                break



if __name__ == '__main__':
    #net0 = network.DriveNet960x544() 
    #net0 = network.Surrond0831()
    #net0 = network.Inception3b()
    g_param = GlobalParam()
    net0 = network.TestBigNet()
    splitTest = SplitNet(g_param, net0)
    #print net0.check_module_size('data0')
    if net0.sorted:
        splitTest.split_net()
        splitTest.print_result()


