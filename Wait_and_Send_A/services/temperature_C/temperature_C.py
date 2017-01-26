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
from random import randrange
import sys
##sys.path.append(os.path.abspath("/home/pi/Desktop/Wait_and_Send_A/services/temperature_B"))
##from get_temperature import listen

def listen(name,timeout):
    listen_txt = ''
    exitflag = 0
    while True:
        while ser.inWaiting()>0:
            t.sleep(0.005)
            listen_txt += ser.read(1)
        if listen_txt !='':
            temp_txt = listen_txt[-7:-3]
            return temp_txt
            listen_txt = ''
        if (exitflag == 1):
            exitflag = 0
            thread.exit()

def __init__(self):
    self.seq = 0
def getNextSeqNo(self):
    self.seq +=1
    return format(self.seq,'010d')

def CONNECTION_on(dst_addr):
    acknowledge = str(packet_type[7]+src_addr+dst_addr+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge

def CRC_calculate(payload):
    k = binascii.crc32(payload)
    h = abs(k) % (1<<32)
    s = bin(abs(h))
    crc="".join(value for index, value in enumerate(s[:26]) if index % 2 == index % 4 ==1)
    return crc


transmission_random = [4,7]
random_index = randrange(0,len(transmission_random))

# end of listen thread function

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',       # Either something COM1 for Windows or /dev/ttyUSB0 fir Linux/RasPi
    baudrate= 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    # writeTimeout = 2,
    timeout = 4,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False
)

#packet_type = [invite,ready, ACK,  NACK,rand_bytes,image, GPS, temperature]
packet_type = ['0000','0001','0010','0011','0100','0101','0110','0111']
src_addr = "0A"
dst_addr = "0B"
seq_num = format(0,'04d')

real_dst_addr = "0C"
mock_payload_sent = format(0,'0155d')
# input = CONNECTION_on(real_dst_addr)# packet_type[7] (temperature) with conn. on
# ser.write(input)
# t.sleep(1.5)

os.system("clear")
print 'Temperature is Sending to ', real_dst_addr

input = 1
exitflag =0

i = 0
n = 2000

packet_type_sent_array = []
seq_num_array = []
payload_array = []
crc_array = []
src_addr_array = []
dst_addr_array = []
real_dst_addr_array = []
time_sent_array = []
total_packet_send = 0
last_payload_sent='0000'

packet_type_recv_array = []
src_addr_recv_array = []
dst_addr_recv_array = []
real_dst_addr_recv_array = []
ack_recv_array = []
seq_num_recv_array = []
time_recv_array = []

while 1:
    try:
        numbytes = ser.inWaiting()
        msg = ''
        msg += ser.readline(180)
        t.sleep(0.001)
        packet_type_recv = msg[:4]
        src_addr_recv = msg[4:6]
        dst_addr_recv = msg[6:8]
        real_dst_addr_recv = msg[8:10]
        # ack_recv = msg[10:13]
        seq_num_recv = msg[10:14]
        time_recv = datetime.datetime.today()

        packet_type_recv_array.insert(n,packet_type_recv)
        packet_type_recv_array = packet_type_recv_array[-n:]
        src_addr_recv_array.insert(n,src_addr_recv)
        src_addr_recv_array = src_addr_recv_array[-n:]
        dst_addr_recv_array.insert(n,dst_addr_recv)
        dst_addr_recv_array = dst_addr_recv_array[-n:]
        real_dst_addr_recv_array.insert(n, real_dst_addr_recv)
        real_dst_addr_recv_array = real_dst_addr_recv_array[-n:]
        # ack_recv_array.insert(n, ack_recv)
        # ack_recv_array = ack_recv_array[-n:]
        seq_num_recv_array.insert(n, seq_num_recv)
        seq_num_recv_array = seq_num_recv_array[-n:]

        time_recv_array.insert(n,time_recv)

        with open('/home/pi/Desktop/Wait_and_Send_A/services/temperature_C/packets_recv_frm_AlltoA.csv','w') as f:
           		writer = csv.writer(f,delimiter='\t');
        		writer.writerows(zip(time_recv_array,packet_type_recv_array,src_addr_recv_array,dst_addr_recv_array,real_dst_addr_recv_array,seq_num_recv_array))

        if packet_type_recv == packet_type[2]:
            if dst_addr_recv == src_addr:
                t.sleep(0.5)
                print 'Transaction in Progress...'
                os.system("clear")
                print 'ACK received. Sending Packets', '\n'
                total_packet_send = 0
                listen_txt = ''
                input1 = 'ER_CMD#T7'
                ser.write(input1)
                t.sleep(0.005)
                input2 = 'ACK'
                ser.write(input2)
                temperature = listen("Listen",0.005)
                t.sleep(1)
                #degree = u'\N{DEGREE SIGN}' + 'C'
                #degree = chr(176) + 'C'
                print 'The temperature is : ', str(temperature), 'C'
                try:
                    test = float(temperature)
                    payload = temperature
                    seq_num = str(format(i,'04d'))
                    print i
                    k = binascii.crc32(payload)
                    h = abs(k) % (1<<32)
                    s = bin(abs(h))
                    crc="".join(value for index, value in enumerate(s[:26]) if index % 2 == index % 4 ==1)
                    seq_num_array.insert(n,seq_num)
                    seq_num_array = seq_num_array[-n:]
                    payload_array.insert(n,payload)
                    payload_array = payload_array[-n:]
                    list = zip(seq_num_array,payload_array)
                    time_sent = datetime.datetime.today()
                    src_addr_array.insert(n,src_addr)
                    src_addr_array = src_addr_array[-n:]
                    dst_addr_array.insert(n,dst_addr)
                    dst_addr_array = dst_addr_array[-n:]
                    real_dst_addr_array.insert(n,real_dst_addr)
                    real_dst_addr_array = real_dst_addr_array[-n:]
                    crc_array.insert(n,crc)
                    crc_array = crc_array[-n:]
                    packet_type_sent_array.insert(n,packet_type[7])
                    packet_type_sent_array = packet_type_sent_array[-n:]
                    time_sent_array.insert(n,time_sent)
                    if payload == '0000':
                        payload = max(payload_array[-50:])
                    else:
                        pass
                    with open('/home/pi/Desktop/Wait_and_Send_A/services/temperature_C/packets_sent_frm_AforC.csv','w') as f:
                                writer = csv.writer(f,delimiter='\t');
                                writer.writerows(zip(time_sent_array,packet_type_sent_array,src_addr_array,dst_addr_array,real_dst_addr_array,seq_num_array,payload_array,crc_array))

                    print 'Sending the fresh payload : ', payload
                    input = str(packet_type[7]+src_addr+dst_addr+real_dst_addr+seq_num+payload+mock_payload_sent+crc)
                    ser.write(input)
                    t.sleep(2)
                    last_payload_sent = payload
                    i = i+1
                    print 'Fresh packets: ',input
                    # t.sleep(4)
                    pass
                except ValueError:
                    payload = last_payload_sent
                    seq_num = str(format(i,'04d'))
                    print i
                    k = binascii.crc32(payload)
                    h = abs(k) % (1<<32)
                    s = bin(abs(h))
                    crc="".join(value for index, value in enumerate(s[:26]) if index % 2 == index % 4 ==1)
                    seq_num_array.insert(n,seq_num)
                    seq_num_array = seq_num_array[-n:]
                    payload_array.insert(n,payload)
                    payload_array = payload_array[-n:]
                    list = zip(seq_num_array,payload_array)
                    print 'Sending the last payload : ', payload
                    input = str(packet_type[7]+src_addr+dst_addr+real_dst_addr+seq_num+payload+mock_payload_sent+crc)
                    ser.write(input)
                    t.sleep(2)

                    i = i+1
                    pass
                pass
            pass

        elif packet_type_recv == packet_type[3]:
            if dst_addr_recv == src_addr:
                if seq_num_recv in seq_num_array:
                    os.system("clear")
                    # t.sleep(0.005)
                    v = seq_num_array.index(seq_num_recv)
                    print 'NACK received. Retransmitting'
                    l = binascii.crc32(payload_array[v])
                    m = abs(l) % (1<<32)
                    p = bin(abs(m))
                    crc_retransmit = "".join(value for index, value in enumerate(p[:26]) if index % 2 == index % 4 ==1)
                    input = str(packet_type[7]+src_addr+dst_addr+real_dst_addr+seq_num_recv+payload_array[v]+mock_payload_sent+crc_retransmit)
                    ser.write(input)
                    print 'Retransmitted packets :', input
                    t.sleep(2)
                    total_packet_send = total_packet_send + 1
                    print 'Sent ', total_packet_send, ' time', '\n'
                    random_value = transmission_random[random_index]
                    while total_packet_send == random_value:
                        print 'Connection Lost / System Exhausted. Re-establishing Connection', '\n'
                        t.sleep(0.5)
                        f.close()
                        execfile('/home/pi/Desktop/Wait_and_Send_A/main.py')
                    pass
                pass

    except KeyboardInterrupt:
        t.sleep(1)
        f.close()
        execfile('/home/pi/Desktop/Wait_and_Send_A/main.py')
