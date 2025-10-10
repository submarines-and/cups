#! /usr/bin/python3

import sys
import os
import socket
from bluetooth import *

try:
    device_uri =  os.environ['DEVICE_URI']
except:
    print("Error reading env variable, will use hard coded value")
    device_uri = "phomemo://53480D83AA69"

uri = device_uri.split('://')

if uri[0] != 'phomemo':
    print("bad url")
    exit(1)

a = uri[1]
bdaddr = a[0:2:] + ':' + a[2:4:] + ':' + a[4:6:] + ':' + a[6:8:] + ':' + a[8:10:] + ':' + a[10:12:]

print('DEBUG: ' + sys.argv[0] +' device ' + bdaddr)


# 0 arguments = attempt to connect to printer using hard coded address and print device info if it is available
if len(sys.argv) == 1:
    print('DEBUG: Will scan for available devices...')

    try:
        sock = socket.socket(socket.AF_BLUETOOTH, proto=socket.BTPROTO_RFCOMM)
        sock.connect((bdaddr, 1))

        model = "M02Pro"
        device_make_and_model = 'Phomemo ' + model
        device_id = 'CLS:PRINTER;CMD:EPSON;DES:Thermal Printer;MFG:Phomemo;MDL:'
        print('direct ' + device_uri + ' "' + device_make_and_model + '" "' + device_make_and_model + ' bluetooth ' + bdaddr + '" "' + device_id + model + ' (BT);"')
        exit(0)
    except OSError as btErr:
        print("ERROR: Can't open Bluetooth connection: " + str(btErr), file=sys.stderr)
        exit(1)


# Regular cups invocation
try:
    print('STATE: +connecting-to-device')
    sock = socket.socket(socket.AF_BLUETOOTH, proto=socket.BTPROTO_RFCOMM)
    sock.connect((bdaddr, 1))

    print('STATE: +sending-data')
    
    with os.fdopen(sys.stdin.fileno(), 'rb', closefd=False) as stdin:
        while True:
            data = stdin.read(8192)
            size = len(data)
            if size == 0:
                break
            sock.sendall(data)
            print('DEBUG: sent %d' % (size))

except OSError as btErr:
    print("ERROR: Can't open Bluetooth connection: " + str(btErr), file=sys.stderr)
    exit(1)

except socket.error as SockErr:
    print("ERROR: Cannot write data: " + str(SockErr), file=sys.stderr)
    exit(1)

try:
    # we need to wait the printer answer before closing the socket
    # otherwise the print is stopped
    print('STATE: +receiving-data')
    sock.settimeout(8)
    while True:
        received = sock.recv(28)
        print('DEBUG: ' + " 0x".join("%02x" % b for b in received))
except:
    pass
exit(0)