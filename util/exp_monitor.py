from monitor import monitor_qlen

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser

import sys
import os
import json
import subprocess
import threading
import json
import math
import re
import sys
import os
import random
import csv

parser = ArgumentParser(description="CWND/Queue Monitor")
parser.add_argument('--dir', '-dir',
                    dest="dir",
                    action="store",
                    help="Directory to store outputs",
                    default="results",
                    required=True)
# Expt parameters
args = parser.parse_args()

if not os.path.exists(args.dir):
  os.makedirs(args.dir)
  print "successfully create a directory"
  opt = open("%s/options" % (args.dir, ), 'w')
  print >> opt, json.dumps(vars(args), sort_keys=True, indent=4, separators=(',', ': '))
  opt.close()

def start_tcpprobe():
    "Install tcp_pobe module and dump to file"
    os.system("(rmmod tcp_probe >/dev/null 2>&1); modprobe tcp_probe full=1;")
    print "Monitoring TCP CWND ... will save it to %s/tcpprobe.txt " % args.dir
    Popen("cat /proc/net/tcpprobe > %stcpprobe.txt" %
          args.dir, shell=True)

def qmon():
    monitor = Process(target=monitor_qlen,args=('s0-eth1', 0.1, '%s/qlen.txt' % args.dir ))
    monitor.start()
    print "Monitoring Queue Occupancy ... will save it to %s/qlen.txt " % args.dir
    #raw_input('Press Enter key to stop the monitor--> ')
    sleep(50)
    monitor.terminate()

if __name__ == '__main__':
    start_tcpprobe()
    qmon()
    Popen("killall -9 cat", shell=True).wait()

