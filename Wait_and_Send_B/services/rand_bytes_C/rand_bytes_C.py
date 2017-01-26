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
import re
from random import randrange

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


def CONNECTION_on(dst_addr):
    acknowledge = str(packet_type[4]+src_addr+dst_addr_C+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge

def ACK_send(dst_addr_A):
    ack_send = str(packet_type[2]+ src_addr+dst_addr_A+real_dst_addr+seq_num_recv+mock_payload+mock_crc)
    return ack_send

def NACK_send(NACK):
    nack_send = str(packet_type[3] + src_addr+dst_addr_A+real_dst_addr+NACK+seq_num_recv)
    return nack_send



# end of listen thread function

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',       # Either something COM1 for Windows or /dev/ttyUSB0 fir Linux/RasPi
    baudrate= 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    # writeTimeout = 2,
    timeout = 2,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False
)

transmission_random = [4,7]
random_index = randrange(0,len(transmission_random))

#packet_type= [invite, ready, ACK,  NACK,rand_byte,image, GPS, teperature]
packet_type = ['0000','0001','0010','0011','0100','0101','0110','0111']
src_addr = "0B"
dst_addr_A = "0A"
dst_addr_C = "0C"
real_dst_addr = '0C'

mock_seq_num = format(0, '04d')
mock_payload = format(0, '0159d')
mock_crc = format(0,'07d')

ACK = bytes('111')
NACK = bytes('000')

seq_num_recv = format(0,'04d')

# input = CONNECTION_on(real_dst_addr)# packet_type[4] (rand_bytes) with conn. on to C
# ser.write(input)
# print 'Conn: ', input
# t.sleep(2.5)


os.system("clear")
print 'Random Data is Receiving from ', dst_addr_A
print 'Random Data is Forwarding to ', dst_addr_C

input=1
exitflag = 0

n = 200
packet_type_recv_array = []
src_addr_recv_array = []
dst_addr_recv_array = []
real_dst_addr_recv_array = []
seq_num_recv_array = []
payload_recv_array = []
crc_recv_array= []

seq_num_sent_array = []
payload_sent_array = []
crc_sent_array = []

time_recv_array = []
total_packet_send = 0
last_seq_num_recv = '0000'
i = 0


while 1:
    try:
        numbytes = ser.inWaiting()
        msg = ''
        msg += ser.readline(180)
        print 'msg:', msg
        t.sleep(0.001)
        packet_type_recv = msg[:4]      # 4 bytes
        src_addr_recv = msg[4:6]        # 2 bytes
        dst_addr_recv = msg[6:8]        # 2 bytes
        real_dst_addr_recv = msg[8:10]  # 2 bytes
        seq_num_recv = msg[10:14]       # 4 bytes
        payload_recv = msg[14:-7]       # 159 bytes
        crc_recv = msg[-7:]             # 7 bytes

        packet_length = len((str(msg)))
        if packet_type_recv == packet_type[4]:
            if src_addr_recv == dst_addr_A:
                if dst_addr_recv == src_addr:
                    seq_num_recv_array.insert(n,seq_num_recv)
                    seq_num_recv_array = seq_num_recv_array[-n:]
                    payload_recv_array.insert(n,payload_recv)
                    payload_recv_array = payload_recv_array[-n:]
                    crc_recv_array.insert(n,crc_recv)
                    crc_recv_array = crc_recv_array[-n:]
                    list_recv_A = zip(seq_num_recv_array, payload_recv_array, crc_recv_array)
                    os.system("clear")
                    t.sleep(0.5)
                    print 'Transaction in Progress...'
                    print 'Random Bytes Received from ', src_addr_recv
                    print 'Forwarding Packets to ', dst_addr_C

                    input = str(packet_type[4]+src_addr+dst_addr_C+real_dst_addr+seq_num_recv+payload_recv+crc_recv)
                    ser.write(input)
                    print 'fresh packet forward to C:', input
                    t.sleep(0.5)

                    x = 0
                    last_seq_num_recv = seq_num_recv

                    pass
                pass
            pass

        elif packet_type_recv == packet_type[2]:
            if src_addr_recv == dst_addr_C:
                if dst_addr_recv == src_addr:
                    os.system("clear")

                    print 'ACK Received from ', src_addr_recv
                    print 'Waiting for next packet from ', dst_addr_A
                    input = str(packet_type[2]+ src_addr+dst_addr_A+real_dst_addr+seq_num_recv+mock_payload+mock_crc)
                    ser.write(input)
                    print 'ACK to A :', input
                    t.sleep(1)
                    total_packet_send = 0
                    pass
                pass
            pass


        elif packet_type_recv == packet_type[3]:
            if src_addr_recv == dst_addr_C:
                if dst_addr_recv == src_addr:
                    if seq_num_recv in seq_num_recv_array:
                        os.system("clear")
                        r = seq_num_recv_array.index(seq_num_recv)
                        print 'NACK Received from ',src_addr_recv, '. Retransmitting Packets to ', src_addr_recv
                        input = str(packet_type[4]+src_addr+dst_addr_C+real_dst_addr+seq_num_recv+payload_recv_array[r]+crc_recv_array[r])
                        ser.write(input)
                        print 'NACK response to C :', input
                        t.sleep(0.5)
                        total_packet_send = total_packet_send + 1
                        print 'Sent ', total_packet_send, ' time', '\n'
                        random_value = transmission_random[random_index]
                        while total_packet_send == random_value:
                            print 'Connection Lost / System Exhausted. Re-establishing Connection'
                            t.sleep(0.5)
                            execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')
                        pass
                    pass
                pass
            pass

        elif msg == '':
            if last_seq_num_recv != '0000':
                os.system("clear")
                print 'Nothing received from ', dst_addr_A,'. Sending NACK'
                input = str(packet_type[3]+src_addr + dst_addr_A + real_dst_addr+last_seq_num_recv+mock_payload+mock_crc)
                ser.write(input)
                print 'NACK to A for nothing :', input
                t.sleep(1)
                x = x + 1
                print 'Sent ', x, ' time', '\n'
                random_value = transmission_random[random_index]
                if x == random_value:
                    print '\n', 'Connection Lost / System Exhausted. Re-establishing Connection...', '\n'
                    execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')
                    pass
                pass
            pass


        elif packet_type_recv == packet_type[0]:
            if src_addr_recv == dst_addr_A:
                if dst_addr_recv == src_addr:
                    input = str(packet_type[0]+src_addr+dst_addr_C+real_dst_addr)
                    execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')
                    pass
                pass
            pass


    except KeyboardInterrupt:
        execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')


        if packet_type_recv == packet_type[0]:
            if src_addr_recv == dst_addr_A:
                if dst_addr_recv == src_addr:
                    input = str(packet_type[0]+src_addr+dst_addr_C+real_dst_addr)
                    execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')

    except KeyboardInterrupt:
        execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')
