#!/usr/bin/env python

import argparse
 
def parse_args():
    parser = argparse.ArgumentParser(description = description)
     
    help = The addresses to connect.
    parser.add_argument('addresses',nargs = '*',help = help)
 
    help = The filename to operate on.Default is poetry/ecstasy.txt
    parser.add_argument('filename',help=help)
 
    help = The port to listen on. Default to a random available port.
    parser.add_argument('-p',--port', type=int, help=help)
 
    help = The interface to listen on. Default is localhost.
    parser.add_argument('--iface', help=help, default='localhost')
 
    help = The number of seconds between sending bytes.
    parser.add_argument('--delay', type=float, help=help, default=.7)
 
    help = The number of bytes to send at a time.
    parser.add_argument('--bytes', type=int, help=help, default=10)
 
    args = parser.parse_args();
    return args
 
if __name__ == '__main__':
    args = parse_args()
     
    for address in args.addresses:
        print 'The address is : %s .' % address
     
    print 'The filename is : %s .' % args.filename
    print 'The port is : %d.' % args.port
    print 'The interface is : %s.' % args.iface
    print 'The number of seconds between sending bytes : %f'% args.delay
