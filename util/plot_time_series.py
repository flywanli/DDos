#!/usr/bin/env python
from helper import *
import glob
import sys
from collections import defaultdict
from statsmodels.graphics import utils
from statsmodels.tsa.stattools import acf, acovf

parser = argparse.ArgumentParser()
parser.add_argument('--dir',
                    dest="dir",
                    help="Directory from which outputs of the sweep are read.",
                    required=True)
parser.add_argument('--out',
                    dest="out",
                    help="Generated output figure.",
                    required=True)

args = parser.parse_args()
'''
directory="/home/wanli/TCPDoS/ddos-Aug19-14:06/rto-300-tcp_n-1/"
out="/home/wanli/TCPDoS/freqresult.png"
'''
def plot_fourier(ax, name, label, color, marker):
  xdata = []
  ydata = []
  frequency=[]
  freq=[]
  '''for s in os.listdir(args.dir):
    interval = re.findall('interval-([0-9.]+)', s)
    if len(interval) == 0: continue'''

  with open("%s/packets-%s" % (args.dir, name)) as hGS:
    data = map(lambda x: x.split(', '), hGS.readlines())
    data = filter(lambda x: len(x) > 1, data)
    timestamp=map(lambda x: x[0], data)
    base_time=timestamp[0]
    timestamp=map(lambda x: float(x)-float(base_time),timestamp)
    f=map(lambda x: x[1], data)
    for i in range(len(f)-1):
      freq+=[float(f[i+1])-float(f[i])]
    
    if len(freq)>1:
		pass
    else:
		return
  ax.plot(timestamp[1:],freq,label=label,color=color)


def main():
  fig=plt.figure(figsize=(16,6))
  ax =fig.add_subplot(111)
  plot_fourier(ax,'hGR', None,color='green', marker=None)
  
  period = re.findall('period-([0-9.]+)',args.dir)
  burst  = re.findall('burst-([0-9.]+)',args.dir)
  ax.legend(loc=2, bbox_to_anchor=(1.05, 1))
  ax.set_ylabel("Packets Number")
  ax.set_xlabel("Elaspe Time: attack period %s and burst %s" %(period[0],burst[0]))
  plt.savefig("%s" % (args.out, ))
  

if __name__ == '__main__':
  main()
