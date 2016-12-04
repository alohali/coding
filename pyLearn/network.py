import numpy as np
import Queue
import cnnlayer

class Network(object):
    """Network init, build and sort"""
    def __init__(self, *args):
        if len(args)>=2:
            self.datasize = args[0]
            self.topo_method = args[1]
        else:
            self.datasize = 1
            self.topo_method = "dfs"

        self.layer_map = dict() #string to layer
        self.root   = None
        self.sorted = False
        self.sorted_layers = list() #string

    def insert_layer(self, **kwargs):
        layer = cnnlayer.Layer(self.datasize)
        layer.setParam(**kwargs)
        if not layer.name in self.layer_map:
            self.layer_map[layer.name] = layer
        else:
            raise ValueError,"duplicate layer!"


    def sort_net(self):
        if self.root==None:
            raise ValueError,"No root of net!"
        #I don't know if dfs is better or dfs
        if self.sorted:
            return
        self.sorted = True
        self.__toposort(self.topo_method) 

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
            real_layer = self.layer_map[layer]
            real_layer.module_size = self.__check_module_size(layer)
            for suc in real_layer.suc:
                if suc in self.sorted_layers:
                    continue
                real_suc = self.layer_map[suc]
                indegree = len(real_suc.pre)
                for pre in real_suc.pre:
                    if pre in self.sorted_layers:
                        indegree -= 1
                if indegree==0:
                    list0.put(suc)
        print "sorted_layers,", self.sorted_layers

    def __check_module_size(self, module_root):
        """
            calculate the size of inception module
            toposort by level 
            not sure if the calcution is bug free, just suitable for current modules, need to check
            ##bad func, need to re-write
        """

        list0 = Queue.Queue() #queue
        list0.put(module_root)
        size = 0
        visited = set()

        while not list0.empty():
            layer = list0.get()
            real_layer = self.layer_map[layer]
            if not real_layer.type==cnnlayer.Type.DATA:
                size += 1
            suc_all = real_layer.suc
            if list0.empty():
                if size>len(suc_all):   
                    if len(suc_all)==1:
                        size += 1
                    return size
                if len(suc_all)==1:
                    return size
            visited.add(layer)
            for suc in suc_all:
                if suc in visited:
                    continue
                real_suc = self.layer_map[suc]
                indegree = len(real_suc.pre)
                for pre in real_suc.pre:
                    if pre in visited:
                        indegree -= 1
                if indegree==0:
                    list0.put(suc)


    def get_layer_by_name(self, name):
        if name in self.layer_map:
            return self.layer_map[name]
        else:
            assert 0, "no such layer"

    def get_layer_by_idx(self,idx):
        if not self.sorted:
            raise ValueError,"call after sorting"
        return self.layer_map[ self.sort_net[idx]]

    def lifetime(self):
        assert 0,"Haven't implemented"



class Surrond0831(Network):
    """network surrond0831"""
    def __init__(self, *args):
        super(Surrond0831, self).__init__(args)
        self.root = "data0"
        args = {'name':"data0", 'type':cnnlayer.Type.DATA, 'nchwkpq':[1, 3 , 544, 960, 3 , 544, 960],\
                'pre':[], 'suc':['conv0']}
        self.insert_layer(**args)

        args = {'name':"conv0", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 3 , 544, 960, 16, 272, 480],\
                'pre':["data0"], 'suc':['conv1'],'rsuv':[7, 2], 'pad':3}
        self.insert_layer(**args)

        args = {'name':"conv1", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 16, 272, 480, 56, 136, 240],\
                'pre':["conv0"], 'suc':['conv2'],'rsuv':[3, 2], 'pad':1}
        self.insert_layer(**args)

        args = {'name':"conv2", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 56, 136, 240, 64, 136, 240],\
                'pre':["conv1"], 'suc':['conv3'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)

        args = {'name':"conv3", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 64, 136, 240, 64, 136, 240],\
                'pre':["conv2"], 'suc':['conv4'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)

        args = {'name':"conv4", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 64, 136, 240, 64, 136, 240],\
                'pre':["conv3"], 'suc':['conv5'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)

        args = {'name':"conv5", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 64, 136, 240,104, 68 , 120],\
                'pre':["conv4"], 'suc':['conv6'],'rsuv':[3, 2], 'pad':1}
        self.insert_layer(**args)

        args = {'name':"conv6", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1,104, 68 , 120,112, 68 , 120],\
                'pre':["conv5"], 'suc':[       ],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)

        self.sort_net()

class DriveNet960x544(Network):
    """network surrond0831"""
    def __init__(self,*args):
        super(DriveNet960x544, self).__init__(args)
        self.root = "data0"
        args = {'name':"data0", 'type':cnnlayer.Type.DATA, 'nchwkpq':[1, 3 , 544, 960, 3 , 544, 960],\
                'pre':[], 'suc':['conv0']}
        self.insert_layer(**args)

        args = {'name':"conv0", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 3 , 544, 960, 64, 272, 480],\
                'pre':["data0"], 'suc':['pool0'],'rsuv':[7, 2], 'pad':3}
        self.insert_layer(**args)

        args = {'name':"pool0", 'type':cnnlayer.Type.POOL, 'nchwkpq':[1, 64, 272, 480, 64, 136, 240],\
                'pre':["conv0"], 'suc':['norm0'],'rsuv':[3, 2], 'pad':1}
        self.insert_layer(**args)

        args = {'name':"norm0", 'type':cnnlayer.Type.LRN , 'nchwkpq':[1, 64, 136, 240, 64, 136, 240],\
                'pre':["pool0"], 'suc':['conv1']}
        self.insert_layer(**args)

        args = {'name':"conv1", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 64, 136, 240, 64, 136, 240],\
                'pre':["pool0"], 'suc':['conv2'],'rsuv':[1, 1], 'pad':0}
        self.insert_layer(**args)

        args = {'name':"conv2", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 64, 136, 240, 192, 136, 240],\
                'pre':["conv1"], 'suc':['norm1'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)


        args = {'name':"norm1", 'type':cnnlayer.Type.LRN , 'nchwkpq':[1, 192, 136, 240, 192, 136, 240],\
                'pre':["conv2"], 'suc':['pool1']}
        self.insert_layer(**args)

        args = {'name':"pool1", 'type':cnnlayer.Type.POOL, 'nchwkpq':[1, 192, 136, 240, 192, 68, 120],\
                'pre':["norm1"], 'suc':[],'rsuv':[3, 2], 'pad':1}
        self.insert_layer(**args)

        self.sort_net()

class TestBigNet(Network):
    """network surrond0831"""
    def __init__(self,*args):
        super(TestBigNet, self).__init__(args)
        self.root = "data0"
        args = {'name':"data0", 'type':cnnlayer.Type.DATA, 'nchwkpq':[1, 3 , 544, 960, 3 , 544, 960],\
                'pre':[], 'suc':['conv0']}
        self.insert_layer(**args)

        args = {'name':"conv0", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 3 , 544, 960, 128, 272, 480],\
                'pre':["data0"], 'suc':['pool0'],'rsuv':[7, 2], 'pad':3}
        self.insert_layer(**args)

        args = {'name':"pool0", 'type':cnnlayer.Type.POOL, 'nchwkpq':[1, 128, 272, 480, 128, 136, 240],\
                'pre':["conv0"], 'suc':['norm0'],'rsuv':[3, 2], 'pad':1}
        self.insert_layer(**args)

        args = {'name':"norm0", 'type':cnnlayer.Type.LRN , 'nchwkpq':[1, 128,  136, 240, 128,  136, 240],\
                'pre':["pool0"], 'suc':['conv1']}
        self.insert_layer(**args)

        args = {'name':"conv1", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 128,  136, 240, 128,  136, 240],\
                'pre':["norm0"], 'suc':['conv2'],'rsuv':[1, 1], 'pad':0}
        self.insert_layer(**args)

        args = {'name':"conv2", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 128,  136, 240, 192, 136, 240],\
                'pre':["conv1"], 'suc':['norm1'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)


        args = {'name':"norm1", 'type':cnnlayer.Type.LRN , 'nchwkpq':[1, 192, 136, 240, 192, 136, 240],\
                'pre':["conv2"], 'suc':['pool1']}
        self.insert_layer(**args)

        args = {'name':"pool1", 'type':cnnlayer.Type.POOL, 'nchwkpq':[1, 192, 136, 240, 192, 136, 240,],\
                'pre':["norm1"], 'suc':[],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)

        self.sort_net()


class Inception3b(Network):
    """network surrond0831"""
    def __init__(self,*args):
        super(Inception3b, self).__init__(args)
        self.root = "data0"
        args = {'name':"data0", 'type':cnnlayer.Type.DATA, 'nchwkpq':[1, 256, 68, 120, 256, 68, 120],\
                'pre':[], 'suc':['conv1x1','conv3x3reduce','conv5x5reduce','pool3x3']}
        self.insert_layer(**args)

        """inception 3b"""
        args = {'name':"conv1x1", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 256, 68, 120, 128, 68, 120],\
                'pre':['data0'], 'suc':['pool_output'],'rsuv':[1, 1], 'pad':0}
        self.insert_layer(**args)

        args = {'name':"conv3x3reduce", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 256, 68, 120, 128, 68, 120],\
                'pre':['data0'], 'suc':['conv3x3'],'rsuv':[1, 1], 'pad':0}
        self.insert_layer(**args)

        args = {'name':"conv5x5reduce", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 256, 68, 120, 32, 68, 120],\
                'pre':['data0'], 'suc':['conv5x5'],'rsuv':[1, 1], 'pad':0}
        self.insert_layer(**args)

        args = {'name':"pool3x3", 'type':cnnlayer.Type.POOL, 'nchwkpq':[1, 256, 68, 120, 256, 68, 120],\
                'pre':['data0'], 'suc':['pool_proj'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)

        args = {'name':"conv3x3", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 128, 68, 120, 192, 68, 120],\
                'pre':['conv3x3reduce'], 'suc':['pool_output'],'rsuv':[3, 1], 'pad':1}
        self.insert_layer(**args)

        args = {'name':"conv5x5", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 32, 68, 120, 96, 68, 120],\
                'pre':['conv5x5reduce'], 'suc':['pool_output'],'rsuv':[5, 1], 'pad':2}
        self.insert_layer(**args)

        args = {'name':"pool_proj", 'type':cnnlayer.Type.CONV, 'nchwkpq':[1, 256, 68, 120, 64, 68, 120],\
                'pre':['pool3x3'], 'suc':['pool_output'],'rsuv':[1, 1], 'pad':0}
        self.insert_layer(**args)

        args = {'name':"pool_output", 'type':cnnlayer.Type.POOL, 'nchwkpq':[1, 480, 68, 120, 480, 34, 60],\
                'pre':['conv1x1', 'conv3x3', 'conv5x5', 'pool_proj'], 'suc':[],'rsuv':[3, 2], 'pad':1}
        self.insert_layer(**args)

        self.sort_net()
