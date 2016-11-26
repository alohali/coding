#!/usr/bin/env python

a=[1]


c="aaa"
b=dict()
b[c] = a
raise ValueError,"kfdlsj"
        """

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
        self.Layers = [data0, conv0, pool0, conv1, conv2]  # in dfs+toposort"""
