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

def ACK_send(dst_addr):
    ack_send = str(packet_type[2]+ src_addr+dst_addr+real_dst_addr+seq_num_recv+mock_payload+mock_crc)
    return ack_send

def NACK_send(NACK):
    nack_send = str(packet_type[3] + src_addr+dst_addr+real_dst_addr+NACK+seq_num_recv)
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
    timeout =3,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False
)

transmission_random = [4,7]
random_index = randrange(0,len(transmission_random))


#packet_type= [invite, ready, ACK,  NACK,rand_byte,image, GPS, teperature]
packet_type = ['0000','0001','0010','0011','0100','0101','0110','0111']
src_addr = "0C"
dst_addr = "0B"
real_dst_addr = '0C'

ACK = bytes('111')
NACK = bytes('000')

seq_num_recv = format(0,'04d')
mock_payload = format(0, '0159d')
mock_crc = format(0,'07d')

t.sleep(1)
input = ACK_send(dst_addr) # packet_type[2] ACK to B
ser.write(input)
print 'ACK: ', input

os.system("clear")
print 'Temperature is Receiving from ', dst_addr

input=1
exitflag = 0

n = 2000
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
        payload_recv = msg[14:18]       # 4 bytes
        mock_payload_recv = msg[18:-7]  # 155 bytes
        crc_recv = msg[-7:]             # 7 bytes

        packet_length = len((str(payload_recv)))
        if msg != '':
            if real_dst_addr_recv == src_addr:
                if packet_type_recv == packet_type[7]:
                    k = binascii.crc32(payload_recv)
                    h = abs(k) % (1<<32)
                    s = bin(abs(abs(k) % (1<<32)))
                    crc = "".join(value for index, value in enumerate(s[:26]) if index % 2 == index % 4 == 1)
                    if crc == crc_recv:
                        try:
                            test = float(payload_recv)
                            # if seq_num_recv not in seq_num_recv_array:
                            os.system("clear")
                            src_addr_recv_array.insert(n,src_addr_recv)
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
                            payload_recv_array.insert(n,float(payload_recv))
                            payload_recv_array = payload_recv_array[-n:]
                            max_temperature_array = max(payload_recv_array[-20:])
                            min_temperature_array = min(payload_recv_array[-20:])
                            sum_temperature_array = sum(payload_recv_array[-10:])
                            avg = sum_temperature_array / len(payload_recv_array[-10:])
                            avg_str = str(avg)
                            with open('/home/pi/Desktop/Wait_and_Send_C/services/temperature_C/packets_recv_frm_AtoC_only.csv','w') as f:
                                    writer = csv.writer(f,delimiter='\t');
                                    writer.writerows(zip(time_recv_array,packet_type_recv_array,src_addr_recv_array,dst_addr_recv_array,real_dst_addr_recv_array,seq_num_recv_array,payload_recv_array,crc_recv_array))
                            #degree = u'\N{DEGREE SIGN}' + 'C'
                            print 'Temperature Received. Printing...'
                            print 'Temperature is           : ', payload_recv, 'C'
                            print 'Average Temperature is   : ', avg_str[:5], 'C'
                            print 'Max Temperature          : ', str(max_temperature_array), 'C'
                            print 'Min Temperature          : ', str(min_temperature_array), 'C'
                            print 'Packet Length            : ', str(packet_length)
                            print '\n', 'Sending ACK...', '\n'
                            # t.sleep(1)
                            input = str(packet_type[2]+ src_addr+dst_addr+real_dst_addr_recv+seq_num_recv+mock_payload+mock_crc)
                            ser.write(input)
                            t.sleep(0.05)
                            print 'ACK to B :', input
                            i = 0
                            last_seq_num_recv = seq_num_recv
                            pass

                        except ValueError:
                            input = str(packet_type[2]+ src_addr+dst_addr+real_dst_addr_recv+seq_num_recv+mock_payload+mock_crc)
                            ser.write(input)
                            t.sleep(0.05)
                            pass

                    if crc != crc_recv:
                        print 'CRC error'
                        input = str(packet_type[3]+src_addr+dst_addr+real_dst_addr_recv+last_seq_num_recv+mock_payload+mock_crc)
                        ser.write(input)
                        print 'CRC error to B :', input
                        pass
                    pass
                pass
            pass

        elif msg == '':
            if last_seq_num_recv != '0000':
                os.system("clear")
                print 'Nothing Received. Sending NACK to ', dst_addr
                input = str(packet_type[3]+src_addr + dst_addr + real_dst_addr+last_seq_num_recv+mock_payload+mock_crc)
                ser.write(input)
                print 'NACK to B :', input
                i = i + 1
                t.sleep(2)
                print 'Sent ', i, ' time', '\n'
                random_value = transmission_random[random_index]
                if i == random_value:
                    print '\n', 'Connection Lost / System Exhausted. Re-establishing Connection...', '\n'
                    f.close()
                    execfile('/home/pi/Desktop/Wait_and_Send_C/main.py')
                    pass
                pass
            pass

        if packet_type_recv == packet_type[0]:
            f.close()
            execfile('/home/pi/Desktop/Wait_and_Send_C/main.py')

    except KeyboardInterrupt:
        f.close()
        execfile('/home/pi/Desktop/Wait_and_Send_C/main.py')
