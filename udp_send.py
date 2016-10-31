#!/usr/bin/env python

import sys
import socket
import random
from time import time, sleep

UDP_IP = sys.argv[1]
UDP_PORT = int(sys.argv[2])
BURST = float(sys.argv[3])
INTERVAL = float(sys.argv[4])
RAND = float(sys.argv[5])

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MESSAGE = '1' * 1440
print "random peoridc"
if False:
  start = time()
  while time() - start < 5:
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

rate = (15 * 1024 * 1024)/64.
sleep(0.9)
start_time = time()
rand_num=random.uniform(0,RAND)
while True:
  start_time+= INTERVAL
  next_start_time = start_time+rand_num
  #next_start_time += BURST+ random.uniform(0,INTERVAL)
  start = time()
  bits = 0
  while time() - start < BURST:
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
    bits += len(MESSAGE) * 8
    time_pass = (time() - start)
    if bits / time_pass > rate:
      next_time = bits / rate
      sleep(next_time - time_pass)

  sleep_to = next_start_time - time()
  if sleep_to > 0:
    sleep(sleep_to)
