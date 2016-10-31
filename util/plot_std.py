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


def plot(ax):
    with open("%s/throughput.txt" % (args.dir,)) as f:
      data = map(lambda x: x.split(), f.readlines())
      data = filter(lambda x: len(x) > 1, data)
      xdata = map(lambda x: float(x[4]),data)
      ydata = map(lambda x: float(x[3]),data)
      ax.plot(xdata,ydata, label=None, color='red', marker='o')

def main():
  fig = plt.figure()
  ax = fig.add_axes([0.15, 0.1, 0.75, 0.85])
  plot(ax)
  ax.set_ylabel("Throughput (normalized)")
  ax.set_xlabel("Uniform random seed")
  ax.legend(loc=2, bbox_to_anchor=(1.05, 1))
  plt.savefig("%s" % (args.out, ))

if __name__ == '__main__':
  main()
