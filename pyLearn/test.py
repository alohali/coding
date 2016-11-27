#!/usr/bin/env python



import Queue

q = Queue.LifoQueue()
q.put(0)
q.put(1)
q.put(2)
q.put(3)

while not q.empty():
    print q.get()
print "done",0,1
