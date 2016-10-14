#!/usr/bin/env python

import sys
import socket
from time import time, sleep

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])
BURST = float(sys.argv[3])
INTERVAL = float(sys.argv[4])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

MESSAGE = '1' * 1440

if False:
  start = time()
  while time() - start < 5:
    sock.sendto(MESSAGE, (TCP_IP, TCP_PORT))

rate = 15 * 1024 * 1024.
sleep(0.9)
next_start_time = time()
while True:
  next_start_time += INTERVAL
  start = time()
  bits = 0
  while time() - start < BURST:
    sock.sendto(MESSAGE, (TCP_IP, TCP_PORT))
    bits += len(MESSAGE) * 8
    time_pass = (time() - start)
    if bits / time_pass > rate:
      next_time = bits / rate
      sleep(next_time - time_pass)

  sleep_to = next_start_time - time()
  if sleep_to > 0:
    sleep(sleep_to)
