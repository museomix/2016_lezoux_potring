import serial
import time
ser = serial.Serial('COM3', 9600, timeout=1, parity='N')
print ("wait...")
time.sleep(1)

while 1:
    try:
        line = ser.readline()
        if ('01' in line):
            print line
        #if ('1' in line):
        #    print '1'
        #time.sleep(0.05)
    except ser.SerialTimeoutException:
        print('Data could not be read')
        time.sleep(0.1)
