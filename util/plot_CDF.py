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

def plot_fourier(ax, name, label, color, marker):

  for s in os.listdir(args.dir):
	xdata = []
	ydata = []
	frequency=[]
	freq=[]
	cul_v=[]
	#period = re.findall('period-([0-9.]+)',s)
	burst  = re.findall('burst-([0-9.]+)',s)
	print args.dir
	print s
	  
	with open("%s/%s/packets-%s" % (args.dir,s, name)) as hGS:
		data = map(lambda x: x.split(', '), hGS.readlines())
		data = filter(lambda x: len(x) > 1, data)
		timestamp=map(lambda x: x[0], data)
		f=map(lambda x: x[1], data)
	for i in range(len(f)-1):
	  freq+=[float(f[i+1])-float(f[i])]
	
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
	ax.plot(frequency[0:(len(frequency)/2-1)],cul_v[0:(len(frequency)/2-1)],label='burst %s' %(burst[0]) )

def main():
  fig = plt.figure()
  ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
  plot_fourier(ax, 'hGR', None, color='blue', marker=None)  
  period = re.findall('period-([0-9.]+)',args.dir)
  #burst  = re.findall('burst-([0-9.]+)',args.dir)
  ax.legend(loc=2, bbox_to_anchor=(0.7, 1))
  #ax.legend(loc=2)
  ax.set_ylabel("Amplitude")
  ax.set_xlabel("Cumulatve Spectrum for period %s " %(period[0]))
  #ax.set_xlabel("Cumulatve Spectrum for period ")
  plt.savefig("%s" % (args.out, ))

if __name__ == '__main__':
  main()
