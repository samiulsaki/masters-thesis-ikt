#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time as t
import serial
import thread
import os
import random
import math
import struct,binascii
import csv
##from time import gmtime,strftime
import datetime



def listen(name,timeout):
    listen_txt = ''
    exitflag = 0
    while True:
        while ser.inWaiting()>0:
            t.sleep(0.005)
            listen_txt += ser.read(1)
        if listen_txt !='':
            print listen_txt
            listen_txt = ''
        if (exitflag == 1):
            exitflag = 0
            thread.exit()

def PACKET_invite(real_dst_addr):
    invite = str(packet_type[0]+src_addr+dst_addr+real_dst_addr)
    return invite

def RECV_ready(ACK_ready):
    ready = str(packet_type[1]+src_addr+dst_addr+real_dst_recv)
    return ready

def CONNECTION_on_rand_bytes_C(real_dst_addr):
    acknowledge = str(packet_type[4]+src_addr+dst_addr+real_dst_addr)
    return acknowledge

def CONNECTION_on_image_C(dst_addr):
    acknowledge = str(packet_type[5]+src_addr+dst_addr+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge

def CONNECTION_on_GPS_C(dst_addr):
    acknowledge = str(packet_type[6]+src_addr+dst_addr+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge

def CONNECTION_on_temperature_C(dst_addr):
    acknowledge = str(packet_type[7]+src_addr+dst_addr+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',       # Either something COM1 for Windows or /dev/ttyUSB0 fir Linux/RasPi
    baudrate= 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout = 1,
    timeout = 4,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False
)

#packet_type = [invite,ready, ACK,  NACK,rand_byte,image, GPS, temperature]
packet_type = ['0000','0001','0010','0011','0100','0101','0110','0111']
src_addr = "0A"
seq_num = format(0,'010d')
serv_type = ['0','1']

input = 1
exitflag =0

while 1:
    os.system("clear")
    if ser.inWaiting() == 0:
        nodes = {"B","C"}
        print 'Hello there!'
        print 'To whom you like to send? B/C ?'
        print '   ( BTW You are Node A )'
        print '---------------------------------'
        input = raw_input(':')
        dst_addr = '0B'
        real_dst_addr = '0' + input
        if input in nodes:
            print 'Requesting Connection to ', real_dst_addr
            input = PACKET_invite(real_dst_addr)
            ser.write(input)
            t.sleep(1)
        else:
            print 'Wrong Format/Destination.'
            print '(Type only Capital B/C)'
            t.sleep(0.5)
            pass
        pass
    if ser.inWaiting() > 0:
        try:
            numbytes = ser.inWaiting()
            msg = ''
            msg += ser.readline(10)
            t.sleep(0.001)
            packet_type_recv = msg[:4]
            src_addr_recv = msg[4:6]
            dst_addr_recv = msg[6:8]
            real_dst_addr_recv = msg[8:10]

            if packet_type_recv == packet_type[1]:
                if dst_addr_recv == src_addr:
                    os.system("clear")
                    print 'Connection Running with ', src_addr_recv + '...'
                    print 'What Do You Like To Send?'
                    print 'Press 1 for random bytes'
                    print 'Press 2 for Image'
                    print 'Press 3 for GPS'
                    print 'Press 4 for temperature'
                    input = raw_input(':')
                    if real_dst_addr == '0B':
                        if input == '1':
                            print input, ' Selected. Sending random bytes to B...'
                            execfile('/home/pi/Desktop/Wait_and_Send_A/services/rand_bytes_B/rand_bytes_B.py')
                        elif input == '2':
                            print input, ' Selected. Sending image to B...'
                            execfile('/home/pi/Desktop/Wait_and_Send_A/services/image_B/image_B.py')
                        elif input == '3':
                            print input, ' Selected. Sending GPS to B...'
                            execfile('/home/pi/Desktop/Wait_and_Send_A/services/GPS_B/GPS_B.py')
                        elif input == '4':
                            print input, ' Selected. Sending temperature to B...'
                            execfile('/home/pi/Desktop/Wait_and_Send_A/services/temperature_B/temperature_B.py')
                        else:
                            print 'Wrong key chosen. Start Again'
                            t.sleep(0.5)
                            pass
                        pass
                    if real_dst_addr== '0C':
                        if input == '1':
                            dst_addr = '0B'
                            real_dst_addr = "0C"
                            input1 = CONNECTION_on_rand_bytes_C(real_dst_addr) # packet_type[4] (rand_bytes) with conn. on to B
                            ser.write(input1)
                            t.sleep(4)
                            print input, ' Selected. Sending random bytes to C...'
                            execfile('/home/pi/Desktop/Wait_and_Send_A/services/rand_bytes_C/rand_bytes_C.py')
                        elif input == '2':
                            dst_addr = '0B'
                            real_dst_addr = "0C"
                            input2 = CONNECTION_on_image_C(real_dst_addr) # packet_type[5] (image) with conn. on to B
                            ser.write(input2)
                            t.sleep(4)
                            print input, ' Selected. Sending image to C...'
                            execfile('/home/pi/Desktop/Wait_and_Send_A/services/image_C/image_C.py')
                        elif input == '3':
                            dst_addr = '0B'
                            real_dst_addr = "0C"
                            input3 = CONNECTION_on_GPS_C(real_dst_addr) # packet_type[6] (GPS) with conn. on to B
                            ser.write(input3)
                            t.sleep(4)
                            print input, ' Selected. Sending GPS to C...'
                            execfile('/home/pi/Desktop/Wait_and_Send_A/services/GPS_C/GPS_C.py')
                        elif input == '4':
                            dst_addr = '0B'
                            real_dst_addr = "0C"
                            input4 = CONNECTION_on_temperature_C(real_dst_addr) # packet_type[7] (image) with conn. on to B
                            ser.write(input4)
                            t.sleep(4)
                            print input, ' Selected. Sending temperature to C...'
                            execfile('/home/pi/Desktop/Wait_and_Send_A/services/temperature_C/temperature_C.py')
                        else:
                            print 'Wrong key chosen. Start Again'
                            t.sleep(0.5)
                            pass
                        pass


        except KeyboardInterrupt:
            t.sleep(1)
            exit()
