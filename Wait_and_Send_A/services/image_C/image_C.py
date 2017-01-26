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

def __init__(self):
    self.seq = 0
def getNextSeqNo(self):
    self.seq +=1
    return format(self.seq,'010d')

def CONNECTION_on(dst_addr):
    acknowledge = str(packet_type[5]+src_addr+dst_addr+real_dst_addr)#+mock_seq_num+mock_payload+mock_crc)
    return acknowledge


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

f = open('/home/pi/Desktop/Wait_and_Send_A/services/image_C/apple_C.jpg','rb')
# f = open('/home/pi/Desktop/Wait_and_Send_A/services/image_C/pi_C.png','rb')
byte_read_image = f.read()
t.sleep(0.005)
nf = open('/home/pi/Desktop/Wait_and_Send_A/services/image_C/temp_image_byte_C.txt','wb')
nf.write(byte_read_image)
t.sleep(0.005)
f.close()
nf.close()
rf = open('/home/pi/Desktop/Wait_and_Send_A/services/image_C/temp_image_byte_C.txt','rb')
byte = rf.read()
t.sleep(0.005)

#packet_type = [invite,ready, ACK,  NACK,rand_bytes,image, GPS, temperature]
packet_type = ['0000','0001','0010','0011','0100','0101','0110','0111']
src_addr = "0A"
dst_addr = "0B"
seq_num = format(0,'04d')


real_dst_addr = "0C"


os.system("clear")
print 'Image is Sending to ', real_dst_addr

input = 1
exitflag =0

i = 0
a = 0
n = 200

packet_type_sent_array = []
seq_num_array = []
payload_array = []
crc_array = []
src_addr_array = []
dst_addr_array = []
real_dst_addr_array = []
time_sent_array = []
total_packet_send = 0

packet_type_recv_array =[]
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

        with open('/home/pi/Desktop/Wait_and_Send_A/services/image_C/packets_recv_frm_AlltoA.csv','w') as tf:
                writer = csv.writer(tf,delimiter='\t');
                writer.writerows(zip(time_recv_array,packet_type_recv_array,src_addr_recv_array,dst_addr_recv_array,real_dst_addr_recv_array,seq_num_recv_array))

        if packet_type_recv == packet_type[2]:
            if dst_addr_recv == src_addr:
                t.sleep(0.5)
                print 'Transaction in Progress...'
                os.system("clear")
                print 'ACK received. Sending Packets','\n'
                total_packet_send = 0
                seq_num = str(format(i,'04d'))
                b = a + 159
                hexadecimal = binascii.hexlify(byte)
                payload = str(hexadecimal[a:b])
                if payload != '':
                    a = b
                    k = binascii.crc32(payload)
                    h = abs(k) % (1<<32)
                    s = bin(abs(h))
                    crc_fresh="".join(value for index, value in enumerate(s[:26]) if index % 2 == index % 4 ==1)

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
                    crc_array.insert(n,crc_fresh)
                    crc_array = crc_array[-n:]
                    packet_type_sent_array.insert(n,packet_type[5])
                    packet_type_sent_array = packet_type_sent_array[-n:]
                    time_sent_array.insert(n,time_sent)
                    with open('/home/pi/Desktop/Wait_and_Send_A/services/image_C/packets_sent_frm_AforC.csv','w') as tf:
                            writer = csv.writer(tf,delimiter='\t');
                            writer.writerows(zip(time_sent_array,packet_type_sent_array,src_addr_array,dst_addr_array,real_dst_addr_array,seq_num_array,payload_array,crc_array))

                    input = str(packet_type[5]+src_addr+dst_addr+real_dst_addr+seq_num+payload+crc_fresh)
                    ser.write(input)
                    i = i+1
                    print 'Fresh packets : ', input
                    t.sleep(3)
                    pass

                if len(payload) < 159:
                    print 'Image sending successful. Switching to main page','\n'
                    rf.close()
                    tf.close()
                    os.remove('/home/pi/Desktop/Wait_and_Send_A/services/image_C/temp_image_byte_C.txt')
                    execfile('/home/pi/Desktop/Wait_and_Send_A/main.py')
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
                    input = str(packet_type[5]+src_addr+dst_addr+real_dst_addr+seq_num_recv+payload_array[v]+crc_retransmit)
                    ser.write(input)
                    print 'Retransmitted packets :', input
                    t.sleep(2)
                    total_packet_send = total_packet_send + 1
                    print 'Sent ', total_packet_send, ' time', '\n'
                    random_value = transmission_random[random_index]
                    while total_packet_send == random_value:
                        print 'Connection Lost / System Exhausted. Re-establishing Connection','\n'
                        t.sleep(0.5)
                        tf.close()
                        execfile('/home/pi/Desktop/Wait_and_Send_A/main.py')
                    pass
                pass

    except KeyboardInterrupt:
        t.sleep(1)
        tf.close()
        execfile('/home/pi/Desktop/Wait_and_Send_A/main.py')
