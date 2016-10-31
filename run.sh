#!/bin/bash

# Exit on any failure
set -e

# Check for uninitialized variables
set -o nounset

ctrlc() {
	killall -9 python
	mn -c
	exit
}

trap ctrlc SIGINT

start=`date`
exptid=`date +%b%d-%H:%M`

rootdir=ddos-$exptid
iperf=/usr/bin/iperf
rm -f last
ln -s $rootdir last

#./http/generator.py --dir ./http/Random_objects

#period=1
minRTO=900
tcp_n=1
period=1.1
burst=0.2
for seed in 0.10 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.90 1.0 1.1; do
  dir=$rootdir/period-$period-tcp_n-$tcp_n/burst-$burst/seed-$seed
  
  python tcp_dos.py \
    --bw-host 15 \
    --bw-net 1.5 \
    --delay 6 \
    --dir $dir \
    --rootdir $rootdir \
    --period $period \
    --iperf $iperf \
    --burst $burst \
    --minRTO $minRTO \
    --tcp-n $tcp_n \
    --randseed $seed

  python ./util/fourier-plot.py --dir $dir --out $dir/$period-$burst-result.png>/dev/null
  python ./util/plot_time_series.py --dir $dir --out $dir/$period-$burst-timeseries.png>/dev/null
  python ./util/plot_queue.py --maxy 100 --miny 0 -f $dir/qlen.txt -o $dir/queue.png >/dev/null
  python ./util/plot_tcpprobe.py -f $dir/tcp_probe.txt -o $dir/tcp_cwnd_iperf.png -p 5001 >/dev/null
  #mn -c
done
#python ./util/plot_tradeoff.py --dir $rootdir --out $rootdir/period$period-tradeoff.png>/dev/null
mn -c
cp bootstrap/result.html last/
echo "Started at" $start
echo "Ended at" `date`
echo "Run: python -m SimpleHTTPServer &"

domain=`curl -s -m 2 http://169.254.169.254/latest/meta-data/public-hostname`
if [ -z $domain ]; then
  domain="IP"
fi
echo "Result is located at http://$domain:8000/last/result.html"
