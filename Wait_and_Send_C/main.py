#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time as t
import serial
import thread
import random
import os
import string
import struct,binascii
import datetime
import csv
from sys import exit

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

def RECV_ready(dst_addr):
    ready = str(packet_type[1]+src_addr+dst_addr+real_dst_addr)
    return ready

def CRC_calculate(payload_recv):
    k = binascii.crc32(payload_recv)
    h = abs(k) % (1<<32)
    s = bin(abs(h))
    crc = "".join(value for index, value in enumerate(s[:26]) if index % 3 == index % 4 ==1)
    return crc

def ACK_send(ACK):
    ack_send = str(packet_type[3]+ src_addr+dst_addr+real_dst_addr+ACK+seq_num_recv)
    return ack_send

def NACK_send(NACK):
    nack_send = str(packet_type[3] + src_addr+dst_addr+real_dst_addr+NACK+seq_num_recv)
    return nack_send


# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',       # Either something COM1 for Windows or /dev/ttyUSB0 fir Linux/RasPi
    baudrate= 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout = 0,
    timeout =1,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False
)


#packet_type= [invite, ready, ACK,  NACK,rand_byte,image, GPS, teperature]
packet_type = ['0000','0001','0010','0011','0100','0101','0110','0111']

src_addr = "0C"
ACK = bytes('111')
NACK = bytes('000')

os.system("clear")
print 'Radio is now in listening mode'
print '    (BTW You are Node C)   '
print '------------------------------', '\n'

input=1
exitflag = 0


while 1:
    numbytes = ser.inWaiting()
    msg = ''
    msg += ser.readline(10)
    # print msg
    packet_type_recv = msg[:4]
    src_addr_recv = msg[4:6]
    dst_addr_recv = msg[6:8]
    real_dst_addr_recv = msg[8:10]
    if packet_type_recv == packet_type[0]:
        if real_dst_addr_recv == src_addr:
            if src_addr_recv == '0B':
                os.system("clear")
                print 'Connection Requested from ', src_addr_recv, ' for ', dst_addr_recv, '\n'
                print 'Waiting for the service type selection','\n'
                dst_addr = src_addr_recv
                real_dst_addr = '0C'
                input = RECV_ready(dst_addr) # sending ready (packet_type[1] to B
                ser.write(input)
                t.sleep(0.005)
                pass
            pass
        pass
    if packet_type_recv == packet_type[4]:
        os.system("clear")
        if src_addr_recv == '0B':
            print 'Connection Established with ', src_addr_recv, '\n'
            if real_dst_addr_recv == '0C':
                t.sleep(3.6)
                execfile('/home/pi/Desktop/Wait_and_Send_C/services/rand_bytes_C/rand_bytes_C.py')
                exit()
                pass
    elif packet_type_recv == packet_type[5]:
        os.system("clear")
        if src_addr_recv == '0B':
            print 'Connection Established with ', src_addr_recv, '\n'
            if real_dst_addr_recv == '0C':
                t.sleep(3.6)
                execfile('/home/pi/Desktop/Wait_and_Send_C/services/image_C/image_C.py')
                exit()
                pass
    elif packet_type_recv == packet_type[6]:
        os.system("clear")
        if src_addr_recv == '0B':
            print 'Connection Established with ', src_addr_recv, '\n'
            if real_dst_addr_recv == '0C':
                t.sleep(3.6)
                execfile('/home/pi/Desktop/Wait_and_Send_C/services/GPS_C/GPS_C.py')
                pass
    elif packet_type_recv == packet_type[7]:
        os.system("clear")
        if src_addr_recv == '0B':
            print 'Connection Established with ', src_addr_recv, '\n'
            if real_dst_addr_recv == '0C':
                t.sleep(3.6)
                execfile('/home/pi/Desktop/Wait_and_Send_C/services/temperature_C/temperature_C.py')
                pass
