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
  cul_v=[]
  '''for s in os.listdir(args.dir):
    interval = re.findall('interval-([0-9.]+)', s)
    if len(interval) == 0: continue'''

  with open("%s/packets-%s" % (args.dir, name)) as hGS:
    #data = map(lambda x: x.split(', ')[1].split('\n')[0], hGS.readlines())
    #data = filter(lambda x: len(x) > 1, data)
    data = map(lambda x: x.split(', '), hGS.readlines())
    data = filter(lambda x: len(x) > 1, data)
    timestamp=map(lambda x: x[0], data)
    f=map(lambda x: x[1], data)
    for i in range(len(f)-1):
      freq+=[float(f[i+1])-float(f[i])]
    #print freq
    #ax.plot(timestamp[1:],freq)
    
    '''if len(data) < 2:
      print "%s" % (interval[0], )
      continue'''
    
    #data=np.array(data)
    #data=[float(value) for value in data]
    #print data
    if len(freq)>1:
		acf_value=acf(freq,nlags=len(freq),unbiased=True)
    #print acf_value
		sp=np.fft.fft(acf_value)
		frequency=np.fft.fftfreq(len(freq),0.05)
    #print "the content of frequency is %f " %frequency
		for i in range(0,len(frequency)/2):
			cul_v+=[np.sum(np.abs(sp[0:i]))/np.sum(np.abs(sp[0:(len(frequency)/2-1)]))]
    else:
		return

  #data = sorted(zip(freq, sp), lambda x, y: 1 if x[0] - y[0] > 0 else -1)
  #data=zip(timestamp,frequency)
  #ax.plot(*zip(*data), label=label, color=color, marker=marker)
  #ax.plot(freq[0:len(freq)/2],2.0/len(freq)*np.abs(sp[0:len(freq)/2]), label=label, color=color, marker=marker)
  #print "the length of freq is %f" % len(frequency)
  ax.plot(frequency[0:len(frequency)/2],2.0/len(freq)*np.abs(sp[0:len(frequency)/2]),label=label, color=color, marker=marker)
  #ax.plot(frequency[0:(len(frequency)/2-1)],cul_v[0:(len(frequency)/2-1)],label='Culmutive value', color='red',marker='*')

def main():
  fig = plt.figure()
  ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

  plot_fourier(ax, 'hGR', None, color='blue', marker=None)
  #plot_throughput('hBR', 'Attacker UDP', color='blue', marker='o')
  
  period = re.findall('period-([0-9.]+)',args.dir)
  burst  = re.findall('burst-([0-9.]+)',args.dir)
  ax.legend(loc=2, bbox_to_anchor=(1.05, 1))
  ax.set_ylabel("Amplitude")
  ax.set_xlabel("Frequecy with period %s and burst %s" %(period[0],burst[0]))
  #ax.set_xlabel("Culmalative value")
  plt.savefig("%s" % (args.out, ))

if __name__ == '__main__':
  main()
