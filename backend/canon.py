#! /usr/bin/python3

import sys
import os

try:
    print('STATE: +sending-data')

        

except OSError as ex:
    print("ERROR: System: " + str(ex), file=sys.stderr)
    exit(1)

except:
    pass

exit(0)