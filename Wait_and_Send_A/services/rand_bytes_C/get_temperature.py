#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import time
import serial
import thread

#exitflag = 0

def listen(name,timeout):
    listen_txt = ''
    exitflag = 0    
    while True:
        while ser.inWaiting()>0:
            time.sleep(0.005)
            listen_txt += ser.read(1)
##            print listen_txt
        if listen_txt !='':
            temp_txt = listen_txt[-7:-3]
            return temp_txt
            listen_txt = ''
##            return listen_txt
        if (exitflag == 1):
            exitflag = 0
            thread.exit()
        
            
            
# end of listen thread function
        
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',       # Either something COM1 for Windows or /dev/ttyUSB0 fir Linux/RasPi
    baudrate= 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout = 0,
    timeout = 1,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False
)

input=1

exitflag = 0
##thread.start_new_thread( listen ,("Listen",5,))

##clear = "\n" * 100
##print clear



while 1 :
##    thread.start_new_thread( listen ,("Listen",5,))
    out = ''
    input1 = 'ER_CMD#T7'
    ser.write(input1)
    time.sleep(0.005)
    while ser.inWaiting() > 0:
        time.sleep(0.005)
        input2 = 'ACK'
        ser.write(input2)
        out += ser.read(1)
        temperature = listen("Listen",1)
        degree = u'\N{DEGREE SIGN}' + 'C'
        print("\nThe temperature is : " + str(temperature)+ degree)
        out = ''
        temperature = ''
        time.sleep(1)
        pass
