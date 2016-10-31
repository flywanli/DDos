#!/usr/bin/python

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg
from mininet.util import dumpNodeConnections

from subprocess import Popen, PIPE
from time import sleep, time
from multiprocessing import Process
from argparse import ArgumentParser
from util.monitor import monitor_qlen
from util.helper import stdev, avg

import termcolor as T
import subprocess
import threading
import json
import math
import re
import sys
import os
import random
import csv


#lib to do acf and fft
import numpy as np

from statsmodels.graphics import utils
from statsmodels.tsa.stattools import acf, acovf



# Number of samples to skip for reference util calibration.
CALIBRATION_SKIP = 10

# Number of samples to grab for reference util calibration.
CALIBRATION_SAMPLES = 30

def cprint(s, color):
  """Print in colorfrom monitor import monitor_qlen

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
     s: string to print
     color: color to use"""
  sys.stdout.write(T.colored(s, color))
  sys.stdout.flush()

# Parse arguments
parser = ArgumentParser(description="Buffer sizing tests")
parser.add_argument('--tcp-n', '-t',
                    dest="tcp_n",
                    type=int,
                    action="store",
                    help="Number of TCP flow",
                    default=1)

parser.add_argument('--burst',
                    dest="burst",
                    type=float,
                    action="store",
                    help="Burst length of the attack in seconds",
                    required=True)

parser.add_argument('--minRTO',
                    dest="minRTO",
                    type=float,
                    action="store",
                    help="Min RTO in milliseconds",
                    required=True)

parser.add_argument('--bw-host', '-B',
                    dest="bw_host",
                    type=float,
                    action="store",
                    help="Bandwidth of host links in Mbits",
                    required=True)

parser.add_argument('--bw-net', '-b',
                    dest="bw_net",
                    type=float,
                    action="store",
                    help="Bandwidth of network link ib Mbits",
                    required=True)

parser.add_argument('--delay',
                    dest="delay",
                    type=float,
                    help="Delay of host links in milliseconds",
                    default=87)

parser.add_argument('--dir', '-d',
                    dest="dir",
                    action="store",
                    help="Directory to store outputs",
                    default="results",
                    required=True)

parser.add_argument('--rootdir', '-rootdir',
                    dest="rootdir",
                    action="store",
                    help="Directory to store throughput results",
                    default="results",
                    required=True)

parser.add_argument('--period',
                    dest="period",
                    type=float,
                    action="store",
                    help="Attack period in seconds",
                    required=True)

parser.add_argument('--cong',
                    dest="cong",
                    help="Congestion control algorithm to use",
                    default="bic")

parser.add_argument('--iperf',
                    dest="iperf",
                    help="Path to custom iperf",
                    required=True)

parser.add_argument('--http',
                    dest="http",
                    action='store_true',
                    default=False,
                    help="Run HTTP test")

parser.add_argument('--debug',
                    dest="debug",
                    action='store_true',
                    default=False,
                    help="Print debug messages")
                    
parser.add_argument('--randseed', '-r',
                    dest="rand_seed",
                    type=float,
                    action="store",
                    help="Random seed",
                    required=True)

# Expt parameters
args = parser.parse_args()

CUSTOM_IPERF_PATH = args.iperf
assert(os.path.exists(CUSTOM_IPERF_PATH))

if not os.path.exists(args.dir):
  os.makedirs(args.dir)
  opt = open("%s/options" % (args.dir, ), 'w')
  print >> opt, json.dumps(vars(args), sort_keys=True, indent=4, separators=(',', ': ')) ####Need futher understanding
  opt.close()

# Topology to be instantiated in Mininet
'''
class NetworkTopo(Topo):
  def __init__(self, switch_bw, switch_delay, host_bw, queue_size):
    # Add default members to class.
    super(NetworkTopo, self).__init__()
    self.switch_bw = switch_bw
    self.host_bw = host_bw
    self.switch_delay = switch_delay
    self.queue_size = queue_size
    self.create_topology()

  def create_topology(self):
    hGoodSender = self.addHost('hGS')
    hGoodReceiver = self.addHost('hGR')
    
    

    #hBadSender1 = self.addHost('hBS1')
    #hBadSender2 = self.addHost('hBS2')
    #hBadSender3 = self.addHost('hBS3')
    hBadReceiver = self.addHost('hBR')
    

    sS = self.addSwitch('s0')
    sR = self.addSwitch('s1')
    #sC means switch cluster
    sC = self.addSwitch('s3')
    
    for h in range(64):
			host = self.addHost('hBS%s' % (h + 1))
			self.addLink(host, sC, bw=self.host_bw/64)

    self.addLink(sS, sR, bw=self.switch_bw,
                         delay=self.switch_delay,
                         max_queue_size=math.ceil(self.queue_size / (1440.)))#why is 1440
    self.addLink(hGoodSender, sS, bw=self.host_bw)
    self.addLink(hGoodReceiver, sR, bw=self.host_bw)
    self.addLink(sC,sS,bw=self.switch_bw)
    #self.addLink(hBadSender1, sS, bw=self.host_bw)
    #self.addLink(hBadSender2, sS, bw=self.host_bw)
    #self.addLink(hBadSender3, sS, bw=self.host_bw)
    self.addLink(hBadReceiver, sR, bw=self.host_bw)'''

class NetworkTopo(Topo):
  def __init__(self, switch_bw, switch_delay, host_bw, queue_size):
    # Add default members to class.
    super(NetworkTopo, self).__init__()
    self.switch_bw = switch_bw
    self.host_bw = host_bw
    self.switch_delay = switch_delay
    self.queue_size = queue_size
    self.create_topology()

  def create_topology(self):

    sS = self.addSwitch('s0')
    sR = self.addSwitch('s1')
    #sC means switch cluster
    sC = self.addSwitch('s3')
    
    hGoodSender = self.addHost('hGS')
    hGoodReceiver = self.addHost('hGR')   
    hBadReceiver = self.addHost('hBR')   

    self.addLink(sS, sR, bw=self.switch_bw,
                         delay=self.switch_delay,
                         max_queue_size=math.ceil(self.queue_size / (1440.)))#why is 1440
    self.addLink(hGoodSender, sS, bw=self.host_bw)
    self.addLink(hGoodReceiver, sR, bw=self.host_bw)
    self.addLink(sC,sS,bw=self.switch_bw)
    self.addLink(hBadReceiver, sR, bw=self.host_bw)
    for h in range(64):
		host = self.addHost('hBS%s' % (h + 1))
		self.addLink(host, sC, bw=self.host_bw/64)
    

def start_tcpprobe():
  "Install tcp_probe module and dump to file"
  print "Monitoring TCP CWND ... will save it to %s/tcpprobe.txt " % args.dir
  os.system("rmmod tcp_probe 2>/dev/null; modprobe tcp_probe;")
  Popen("cat /proc/net/tcpprobe > %s/tcp_probe.txt" %
        args.dir, shell=True)#where is the tcp_probe.txt

def stop_tcpprobe():
  subprocess.Popen("killall -9 cat", shell=True, stderr=PIPE).wait()
  subprocess.Popen("rmmod tcp_probe", shell=True, stderr=PIPE).wait()

''' 
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
'''

def get_all_txbytes():
  f = open('/proc/net/dev', 'r')
  lines = f.readlines()[2:]
  # Extract TX bytes from:
  #Inter-|   Receive                                                |  Transmit
  # face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
  # lo: 6175728   53444    0    0    0     0          0         0  6175728   53444    0    0    0     0       0          0
  data = map(lambda x: x.split(':'), lines)
  data = map(lambda x: (x[0], (float(x[1].split()[0]), float(x[1].split()[8]))), data)
  return dict(data)
#look the the data and then get a total understand

def get_txbytes(iface, received=False):
  data = get_all_txbytes()
  if iface not in data:
      raise Exception("could not find iface %s in /proc/net/dev:%s" %
                      (iface, data))
  if received:
    return data[iface][0]
  else:
    return data[iface][1]

##########get the number of packets transmitted
def get_all_txpackets():
  f = open('/proc/net/dev', 'r')
  lines = f.readlines()[2:]
  # Extract TX bytes from:
  #Inter-|   Receive                                                |  Transmit
  # face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
  # lo: 6175728   53444    0    0    0     0          0         0  6175728   53444    0    0    0     0       0          0
  data = map(lambda x: x.split(':'), lines)
  data = map(lambda x: (x[0], (float(x[1].split()[1]), float(x[1].split()[9]))), data)
  return dict(data)

def get_txpackets(iface, received=False):
  data = get_all_txpackets()
  if iface not in data:
      raise Exception("could not find iface %s in /proc/net/dev:%s" %
                      (iface, data))
  if received:
    return data[iface][0]
  else:
    return data[iface][1]
###############################################

def stop_all_iperf():
  os.system('killall ' + CUSTOM_IPERF_PATH)

def set_rto_min(host, iface, rto):
  host.popen("ip route change 10.0.0.0/8 dev %s rto_min %s scope link src %s proto kernel" %
                 (iface, rto, host.IP()), shell=True).communicate()

def start_receiver(host, isTCP):
  opt = ""
  if not isTCP:
    opt += "-u"
  host.popen('%s %s -s -p %s > %s/iperf_server-%s.txt' % (CUSTOM_IPERF_PATH, opt, 5001, args.dir, host.name), shell=True)

def start_sender(send, recv, bw=0, seconds=3600):
  send.popen('%s -c %s -p %s -t %f -l 200 -i 1 -yc -Z %s > /dev/null' %
    (CUSTOM_IPERF_PATH, recv.IP(), 5001, seconds, args.cong), shell=True)

class MonitorLinkRate(threading.Thread):
  def __init__(self, hosts):
    super(MonitorLinkRate, self).__init__()
    self.data_points = []
    self.hosts = hosts
    self.files = map(lambda x: open('%s/ss-%s' % (args.dir, x[0].name, ), 'w'), hosts)
    self.f=open('%s/packets-hGR' % (args.dir), 'w')
    self.sema = threading.Semaphore(0)

  def stop(self):
    self.sema.release()

  def run(self):
    while not self.sema.acquire(False):
      start = time()
      self.get_data_point()
      sleep_time = 0.0500 - (time() - start)
      if sleep_time > 0:
        sleep(sleep_time)
    self.f.close() ####################
    for f in self.files:
      f.close()


  """
  ESTAB      0      984640             10.0.0.4:51398             10.0.0.3:5001   rto:1.6 cwnd:254 ssthresh:261
  """
  def get_data_point(self):
    stamp = time()
    txbytes = get_all_txbytes()
    pkt=get_all_txpackets()
    for i, d in enumerate(self.hosts):
      host, iface, received = d[0], d[1], d[2]
      a = txbytes[iface][0 if received else 1]
      pkts=pkt[iface][0 if received else 1]
      p = host.popen('ss -i -n', shell=True, stdout=PIPE)
      data = [p.stdout.readline().rstrip()] + [p.stdout.readline().rstrip()]
      p.kill()
      data = re.split('[ ]+', data[1])
      if i==1:
	#f=open('%s/packets-%s' % (args.dir, d[0].name), 'w')
	print >> self.f, "%s, %s" % (stamp, pkts)
	#f.close()
      '''if len(data)==6:
        print "the length of the data is %d and data is %s" % (len(data),data)'''
      if len(data) < 7: # UDP
        print >> self.files[i], "%s, %s" % (stamp, a)
      else:
        print >> self.files[i], "%s, %s, %s, %s, %s, %s" % (stamp, a, data[1], data[2], data[5].split(':')[1], data[6].split(':')[1])

def run_udp_interval(send, recv, burst, interval):
  return send.popen(['python', 'udp_send.py', recv.IP(), '5001', str(burst), str(interval)])

def calculate_throughput(iface, interval):
  a = get_txbytes(iface)
  sleep(interval)
  b = get_txbytes(iface)
  return (8.0 * (b - a) / interval / 1024 / 1024)

def run_udp(net):
  start_receiver(net.getNodeByName('hBR'), False)
  return run_udp_interval (net.getNodeByName('hBS1'), net.getNodeByName('hBR'), args.burst, args.period)

'''
def run_udp2(net):
  #start_receiver(net.getNodeByName('hBR'), False)
  return run_udp_interval (net.getNodeByName('hBS2'), net.getNodeByName('hBR'), args.burst, args.period)

def run_udp3(net):
  #start_receiver(net.getNodeByName('hBR'), False)
  return run_udp_interval (net.getNodeByName('hBS3'), net.getNodeByName('hBR'), args.burst, args.period)
'''
  
def run_tcp_normal(net,n):
	start_receiver(net.getNodeByName('hBR'),True)
	for i in range(n):
		start_sender(net.getNodeByName('hGS'), net.getNodeByName('hGR'), 1024 * 1024 * 2000, 3600)
	

def run_tcp(net, n):
  iface = 's1-eth2'
  global t
  while True:
    start_receiver(net.getNodeByName('hGR'), True)
    for i in range(n):
      start_sender(net.getNodeByName('hGS'), net.getNodeByName('hGR'), 1024 * 1024 * 2000, 3600)

    cprint("Wait 10 seconds for TCP           \r", 'green')
    sleep(10)
    t = calculate_throughput(iface, 3)
    cprint("TCP Reference Throughput: %f Mbits\n" % (t, ), 'green')
    if t >= float(args.bw_net) * 0.9:
      break
    stop_all_iperf()

def run_tcp_first(net, n):
  cprint("Attack with period %s and burst %s. %s simultaneous TCP(s)\n" % (args.period, args.burst, args.tcp_n), "green")
  set_rto_min (net.getNodeByName('hGS'), 'hGS-eth0', args.minRTO)

  iface = 's1-eth2'
  run_tcp(net, n)
  start_tcpprobe()
  monitor = Process(target=monitor_qlen,args=('s0-eth1', 0.1, '%s/qlen.txt' % args.dir ))
  monitor.start()
  pcap=Popen('./util/pcap %s %s/pcap_savefile.pcap' %(iface,args.rootdir), shell=True, stdout=PIPE)
  #print "Monitoring Queue Occupancy ... will save it to %s/qlen.txt " % args.dir


  try:
    m = MonitorLinkRate([(net.getNodeByName('hGS'), 's0-eth2', True),
                         (net.getNodeByName('hGR'), 's1-eth2', False),
                         (net.getNodeByName('hBR'), 's1-eth3', False)
                         ])
    m.daemon=True
    m.start()
    start_receiver(net.getNodeByName('hBR'), False)
    for i in range(64):
		host=net.getNodeByName('hBS%s' % (i+1))
		host.popen(['python', 'udp_send.py', net.getNodeByName('hBR').IP(), '5001', str(args.burst), str(args.period),str(args.rand_seed)] )	
   
###################################################################
#    for i in range(0,10):
#      packets=get_txpackets(iface)
#      sleep(0.001)
#      cprint("The number of pakcet at time %f is %f \n" %(time(),packets), 'blue')
###################################################################
    throughput = calculate_throughput(iface, 30)
    cprint("TCP Throughput: %f Mbits\n" % (throughput, ), 'yellow')
    result=open("%s/throughput.txt" %(args.rootdir),'a+')
    print>> result, "%s %s %s %s %s" %(args.period,args.burst,t,throughput,args.rand_seed)
    result.close()
  except:
    raise
  finally:
    m.stop()
    pcap.kill()
    monitor.terminate()
    stop_tcpprobe()

def start_webserver(net):
    hGS = net.getNodeByName('hGS')
    proc = hGS.popen("python http/webserver.py", shell=True)
    sleep(1)
    return [proc]

def download(net, objs):
    hGR = net.getNodeByName('hGR')
    hGS = net.getNodeByName('hGS')

    # Start download
    processes = []
    for obj in objs:
      cmd = "curl -o /dev/null -s -w %%{time_total} %s/http/Random_objects/%sPackages" % (hGS.IP(), obj)
      processes += [hGR.popen(cmd, shell=True)]

    # Waiting for each to stop
    output = []
    for p in processes:
      output += [float(p.communicate()[0])]

    return (output)

def measure_baseline(net, objs):
  times = []
  for i in range(10):
    times += [download(net, objs)]
    sleep(3)
  avgs = [avg(x) for x in zip(*times)]
  return avgs

def measure_attack(net, objs):
  times = []
  for i in range(10):
    times += [download(net, objs)]
    sleep(3)
  obj_download_times = [x for x in zip(*times)]
  return obj_download_times

def get_rand_set(size):
    sizes = range(1, 10, 1) + range(10, 100, 10) + range (100, 1000, 100)
    obj_set = []
    for x in range(size):
      obj_set += [random.choice(sizes)]

    return obj_set

def test_http(net):
    # Get Test set
    objs = get_rand_set(30)

    # Measure Baseline
    cprint("Calculate baseline\n", 'green')
    baseline = measure_baseline(net, objs)

    # Measure Attacked HTTP
    cprint("Attack HTTP flow\n", 'green')
    p = run_udp_interval(net.getNodeByName('hBS'), net.getNodeByName('hBR'), args.burst, args.period)
    attack = measure_attack(net, objs)
    p.kill()

    # Normalize
    output = []
    for x in zip(objs, baseline, attack):
      obj = x[0]
      base = x[1]
      attack_times = x[2]
      output += map(lambda t: (obj, (t / base)), attack_times)

    # Output
    with open("%s/http-data.txt" % (args.dir), "w") as f:
      writer = csv.writer(f)
      #output's format = [[1, 2], [3, 4], [2, 2], [3, 3]]
      writer.writerows(output)


def main():
  start = time()
  '''
  topo = NetworkTopo(switch_bw=args.bw_net, host_bw=args.bw_host, switch_delay='%sms' %(args.delay, ), queue_size=23593)
  net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
  net.start()
  dumpNodeConnections(net.hosts)
  net.pingAll()
  #run_tcp_first(net, args.tcp_n)
  net.stop()
  '''
  print "successful excuete"
  try:
    topo = NetworkTopo(switch_bw=args.bw_net, host_bw=args.bw_host, switch_delay='%sms' %(args.delay, ), queue_size=23593)
    #net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net = Mininet(topo=topo,link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    #net.pingAll()
    
    if args.http:
      test_http(net)
    else:
      run_tcp_first(net, args.tcp_n)

  except:
    print "-"*80
    print "Caught exception.  Cleaning up..."
    print "-"*80
    import traceback
    traceback.print_exc()
    raise
  finally:
    stop_all_iperf()
    net.stop()
    #Popen("killall -9 top bwm-ng tcpdump cat mnexec; mn -c", shell=True, stderr=PIPE)
    Popen("killall -9 top bwm-ng tcpdump cat mnexec", shell=True, stderr=PIPE)
    Popen("pgrep -f webserver.py | xargs kill -9", shell=True).wait()
    #stop_tcpprobe()
    end = time()
    cprint("Experiment took %s seconds\n" % (end - start), "yellow")

if __name__ == '__main__':
  if args.debug:
    lg.setLogLevel('debug')
  else:
    lg.setLogLevel('info')
  #main()
  try:
    main()
  except:
    pass
