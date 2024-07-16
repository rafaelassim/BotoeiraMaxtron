import os.path
import time as time

path = '/dev/sdb'

while True:
    check_file = os.path.exists(path)
    stream = os.popen('echo Returned output')
    output = stream.read()
    output

    print(check_file)
    time.sleep(2)