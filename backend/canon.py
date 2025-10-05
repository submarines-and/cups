#! /usr/bin/python3

import sys
import os
import shutil

try:
    tmpFile = "/tmp/a.jpg"

    if os.path.exists(tmpFile):
        print('STATE: +Delete old tmp file')
        os.remove(tmpFile)

    print('STATE: +sending-data')
    
    with os.fdopen(sys.stdin.fileno(), 'rb', closefd=False) as input, open(tmpFile, 'wb') as output:
        shutil.copyfileobj(input, output)
        

except OSError as ex:
    print("ERROR: System: " + str(ex), file=sys.stderr)
    exit(1)

except:
    pass

exit(0)