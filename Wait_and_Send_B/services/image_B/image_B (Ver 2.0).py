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


def ACK_send(ACK):
    ack_send = str(packet_type[2]+ src_addr+dst_addr+real_dst_addr+ACK+seq_num_recv)
    return ack_send

def NACK_send(NACK):
    nack_send = str(packet_type[3] + src_addr+dst_addr+serv_type[1]+NACK+seq_num_recv)
    return nack_send


# end of listen thread function

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',       # Either something COM1 for Windows or /dev/ttyUSB0 fir Linux/RasPi
    baudrate= 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout = 1,
    timeout =2,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False
)

transmission_random = [4,7]
random_index = randrange(0,len(transmission_random))


#packet_type= [invite, ready, ACK,  NACK,rand_byte,image, GPS, teperature]
packet_type = ['0000','0001','0010','0011','0100','0101','0110','0111']
src_addr = "0B"
dst_addr = "0A"
real_dst_addr = '0B'

ACK = bytes('111')
NACK = bytes('000')

f = open('/home/pi/Desktop/Wait_and_Send_B/services/image_B/temp_image_B.txt','wb')

seq_num_recv = format(0,'04d')
input = ACK_send(ACK)
ser.write(input)
t.sleep(0.005)

os.system("clear")
print 'Image is Receiving from', real_dst_addr

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
time_recv_array = []

last_seq_num_recv = '0000'
i = 0

while 1:
    try:
        numbytes = ser.inWaiting()
        msg = ''
        msg += ser.readline(180)
        t.sleep(0.001)
        packet_type_recv = msg[:4]      # 4 bytes
        src_addr_recv = msg[4:6]        # 2 bytes
        dst_addr_recv = msg[6:8]        # 2 bytes
        real_dst_addr_recv = msg[8:10]  # 2 bytes
        seq_num_recv = msg[10:14]       # 4 bytes
        payload_recv = msg[14:-7]       # 159 bytes
        crc_recv = msg[-7:]             # 7 bytes

        packet_length = len((str(msg)))
        if msg != '':
            if real_dst_addr_recv == src_addr:
                if packet_type_recv == packet_type[5]:
                    k = binascii.crc32(payload_recv)
                    h = abs(k) % (1 << 32)
                    s = bin(abs(h))
                    crc = "".join(value for index, value in enumerate(s[:26]) if index % 2 == index % 4 == 1)
                    if crc == crc_recv:
                        os.system("clear")
                        print 'Image Receiving...'
                        print 'Sequence No is  : ', seq_num_recv
                        print 'Payload is      : ', payload_recv
                        print '\n','Sending ACK...','\n'
                        if seq_num_recv not in seq_num_recv_array:
                            # print("YOLO")
                            src_addr_recv_array.insert(n, src_addr_recv)
                            src_addr_recv_array = src_addr_recv_array[-n:]

                            dst_addr_recv_array.insert(n, dst_addr_recv)
                            dst_addr_recv_array = dst_addr_recv_array[-n:]

                            real_dst_addr_recv_array.insert(n, real_dst_addr_recv)
                            real_dst_addr_recv_array = real_dst_addr_recv_array[-n:]


                            packet_type_recv_array.insert(n,packet_type_recv)
                            packet_type_recv_array = packet_type_recv_array[-n:]

                            time_recv = datetime.datetime.today()

                            time_recv_array.insert(n,time_recv)


                            crc_recv_array.insert(n,crc_recv)
                            crc_recv_array = crc_recv_array[-n:]

                            seq_num_recv_array.insert(n,seq_num_recv)
                            seq_num_recv_array = seq_num_recv_array[-n:]
                            payload_recv_array.insert(n,payload_recv)
                            payload_recv_array = payload_recv_array[-n:]
                            list = zip(seq_num_recv_array,payload_recv_array)
                            f.write(payload_recv)
                            pass

                        with open('/home/pi/Desktop/Wait_and_Send_B/services/image_B/packets_recv_frm_AtoB.csv','w') as tf:
                                writer = csv.writer(tf,delimiter='\t');
                                writer.writerows(zip(time_recv_array,packet_type_recv_array,src_addr_recv_array,dst_addr_recv_array,real_dst_addr_recv_array,seq_num_recv_array,payload_recv_array,crc_recv_array))


                        t.sleep(0.05)
                        input = str(packet_type[2]+ src_addr+dst_addr+real_dst_addr+ACK+seq_num_recv)
                        ser.write(input)
                        i = 0
                        last_seq_num_recv = seq_num_recv
                        pass

                    if crc != crc_recv:
                        print 'CRC error'
                        input = str(packet_type[3]+src_addr+dst_addr+real_dst_addr+NACK+last_seq_num_recv)
                        ser.write(input)
                        t.sleep(0.05)
                        pass
                    pass

        elif msg == '':
            if last_seq_num_recv != '0000':
                os.system("clear")
                print 'Nothing Received. Sending NACK'
                input = str(packet_type[3]+src_addr + dst_addr+real_dst_addr+NACK+last_seq_num_recv)
                print(input)
                print 'NACK :', input
                ser.write(input)
                t.sleep(0.005)
                i = i + 1
                print 'Sent ', i, ' time', '\n'
                random_value = transmission_random[random_index]
                if i == random_value:
                    print '\n', 'Connection Lost / System Exhausted. Re-establishing Connection...', '\n'
                    f.close()
                    rf = open('/home/pi/Desktop/Wait_and_Send_B/services/image_B/temp_image_B.txt','rb')
                    byte = rf.read()
                    try:
                        os.system("clear")
                        hexadecimal = binascii.a2b_hex(byte)
                        nf = open('/home/pi/Desktop/Wait_and_Send_B/services/image_B/apple_hexa8.jpg','wb')
                        nf.write(hexadecimal)
                        nf.close()
                        rf.close()
                        os.remove('/home/pi/Desktop/Wait_and_Send_B/services/image_B/temp_image_B.txt')
                        t.sleep(2)
                        print 'Picture Printed'
                        t.sleep(2)
                        tf.close()
                        execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')
                    except TypeError:
                        print 'Not enough data received'
                        t.sleep(2)
                        tf.close()
                        execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')
                        pass
                pass
            pass

        if packet_type_recv == packet_type[0]:
            tf.close()
            execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')

    except KeyboardInterrupt:
        tf.close()
        execfile('/home/pi/Desktop/Wait_and_Send_B/main.py')
