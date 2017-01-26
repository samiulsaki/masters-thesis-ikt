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

def CONNECTION_on_rand_byte_C(dst_addr):
    acknowledge = str(packet_type[4]+src_addr+dst_addr_C+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge

def CONNECTION_on_image_C(dst_addr):
    acknowledge = str(packet_type[5]+src_addr+dst_addr_C+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge

def CONNECTION_on_GPS_C(dst_addr):
    acknowledge = str(packet_type[6]+src_addr+dst_addr_C+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge

def CONNECTION_on_temperature_C(dst_addr):
    acknowledge = str(packet_type[7]+src_addr+dst_addr_C+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge

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
    timeout =0.5,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False
)


#packet_type= [invite, ready, ACK,  NACK,rand_byte,image, GPS, teperature]
packet_type = ['0000','0001','0010','0011','0100','0101','0110','0111']

src_addr = "0B"
ACK = bytes('111')
NACK = bytes('000')

os.system("clear")
print 'Radio is now in listening mode'
print '    (BTW You are Node B)   '
print '------------------------------', '\n'

input=1
exitflag = 0


while 1:
    numbytes = ser.inWaiting()
    msg = ''
    msg += ser.readline(10)
    packet_type_recv = msg[:4]
    src_addr_recv = msg[4:6]
    dst_addr_recv = msg[6:8]
    real_dst_addr_recv = msg[8:10]
    if packet_type_recv == packet_type[0]:
        if dst_addr_recv == src_addr:
            if real_dst_addr_recv == src_addr:
                os.system("clear")
                print 'Connection Requested from 0A for ', real_dst_addr_recv, '\n'
                print 'Waiting for the service type selection','\n'
                dst_addr = src_addr_recv
                real_dst_addr = '0B'
                input = RECV_ready(dst_addr) # sending ready (packet_type[1] to A
                ser.write(input)
                t.sleep(0.005)
                pass
            elif real_dst_addr_recv == '0C':
                os.system("clear")
                print 'Connection Requested from 0A for ', real_dst_addr_recv, '\n'
                print 'Waiting for the service type selection', '\n'
                dst_addr = real_dst_addr_recv
                real_dst_addr = '0C'
                input = PACKET_invite(dst_addr) # sending invitation (packet_type[0]) to C for A
                ser.write(input)
                t.sleep(0.005)
                pass
            pass
        pass
    if packet_type_recv == packet_type[1]:
        if dst_addr_recv == src_addr:
            os.system("clear")
            print 'Connection Running with 0A for ', real_dst_addr_recv
            dst_addr = '0A'
            real_dst_addr = '0C'
            input = RECV_ready(dst_addr) # sending ready (packet_type[1] to A
            ser.write(input)
            t.sleep(0.005)
            pass
    if packet_type_recv == packet_type[4]:
        os.system("clear")
        if src_addr_recv == '0A':
            print 'Connection Established with ', src_addr_recv, '\n'
            if real_dst_addr_recv == '0B':
                execfile('/home/pi/Desktop/Wait_and_Send_B/services/rand_bytes_B/rand_bytes_B.py')
                exit()
                pass
            if real_dst_addr_recv == '0C':
                dst_addr_C = real_dst_addr_recv
                input = CONNECTION_on_rand_byte_C(real_dst_addr_recv)# packet_type[4] (rand_bytes) with conn. on to C
                ser.write(input)
                t.sleep(3.8)
                execfile('/home/pi/Desktop/Wait_and_Send_B/services/rand_bytes_C/rand_bytes_C.py')
                exit()
                pass
    elif packet_type_recv == packet_type[5]:
        os.system("clear")
        if src_addr_recv == '0A':
            print 'Connection Established with ', src_addr_recv, '\n'
            if real_dst_addr_recv == '0B':
                execfile('/home/pi/Desktop/Wait_and_Send_B/services/image_B/image_B.py')
                exit()
                pass
            if real_dst_addr_recv == '0C':
                dst_addr_C = real_dst_addr_recv
                input = CONNECTION_on_image_C(real_dst_addr_recv)# packet_type[5] (image) with conn. on to C
                ser.write(input)
                t.sleep(3.8)
                execfile('/home/pi/Desktop/Wait_and_Send_B/services/image_C/image_C.py')
                exit()
                pass
    elif packet_type_recv == packet_type[6]:
        os.system("clear")
        if src_addr_recv == '0A':
            print 'Connection Established with ', src_addr_recv, '\n'
            if real_dst_addr_recv == '0B':
                execfile('/home/pi/Desktop/Wait_and_Send_B/services/GPS_B/GPS_B.py')
                pass
            if real_dst_addr_recv == '0C':
                dst_addr_C = real_dst_addr_recv
                input = CONNECTION_on_GPS_C(real_dst_addr_recv)# packet_type[6] (GPS) with conn. on to C
                ser.write(input)
                t.sleep(3.8)
                execfile('/home/pi/Desktop/Wait_and_Send_B/services/GPS_C/GPS_C.py')
                pass
    elif packet_type_recv == packet_type[7]:
        os.system("clear")
        if src_addr_recv == '0A':
            print 'Connection Established with ', src_addr_recv, '\n'
            if real_dst_addr_recv == '0B':
                execfile('/home/pi/Desktop/Wait_and_Send_B/services/temperature_B/temperature_B.py')
                pass
            if real_dst_addr_recv == '0C':
                dst_addr_C = real_dst_addr_recv
                input = CONNECTION_on_temperature_C(real_dst_addr_recv)# packet_type[7] (temperature) with conn. on to C
                ser.write(input)
                t.sleep(3.8)
                execfile('/home/pi/Desktop/Wait_and_Send_B/services/temperature_C/temperature_C.py')
                pass
