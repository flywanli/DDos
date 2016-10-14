#!/usr/bin/env python
from helper import *
import glob
import sys
from collections import defaultdict

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


def plot_tradeoff(ax):
    with open("%s/throughput0.5.txt" % (args.dir,)) as f:
      data = map(lambda x: x.split(), f.readlines())
      data = filter(lambda x: len(x) > 1, data)
      xdata = map(lambda x: float(x[1])/float(x[0]),data)
      ydata = map(lambda x: float(x[3])/float(x[2]),data)
      ax.plot(xdata,ydata, label='period=0.5', color='red', marker='o')
    with open("%s/throughput1.1.txt" % (args.dir,)) as f:
      data = map(lambda x: x.split(), f.readlines())
      data = filter(lambda x: len(x) > 1, data)
      xdata = map(lambda x: float(x[1])/float(x[0]),data)
      ydata = map(lambda x: float(x[3])/float(x[2]),data)
      ax.plot(xdata,ydata, label='period=1.1', color='blue', marker='*')
    with open("%s/throughput1.5.txt" % (args.dir,)) as f:
      data = map(lambda x: x.split(), f.readlines())
      data = filter(lambda x: len(x) > 1, data)
      xdata = map(lambda x: float(x[1])/float(x[0]),data)
      ydata = map(lambda x: float(x[3])/float(x[2]),data)
      ax.plot(xdata,ydata, label='period=1.5', color='green', marker='s')

def main():
  fig = plt.figure()
  ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
  plot_tradeoff(ax)
  ax.set_ylabel("Throughput (normalized)")
  ax.set_xlabel("proportion of attack")
  ax.legend(loc=2, bbox_to_anchor=(1.05, 1))
  plt.savefig("%s" % (args.out, ))

if __name__ == '__main__':
  main()
