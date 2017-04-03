#!/usr/bin/env python3
def b():
  def bchange():
    print(b)
  bchange()
  b = 1
  print b

b()
