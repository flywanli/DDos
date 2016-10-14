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

<< 'mycomment'
# minRTO should be change to 1ms
dir=$rootdir/http
python tcp_dos.py \
  --bw-host 15 \
  --bw-net 1.5 \
  --delay 6 \
  --dir $dir \
  --period 1 \
  --iperf $iperf \
  --burst 0.3 \
  --minRTO 900 \
  --tcp-n 1 \
  --http
./util/plot-http.py --dir $dir --out $dir/result.png

for tcp_n in 1 10; do
  for minRTO in 900 300; do
    for period in 0.5 0.6 0.7 0.8 0.9 0.95 1 1.05 1.1 1.15 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2 2.5 3 3.5 4 4.5 5; do
      dir=$rootdir/rto-$minRTO-tcp_n-$tcp_n/interval-$period/
      rm -f last
      ln -s $rootdir last

      python tcp_dos.py \
        --bw-host 15 \
        --bw-net 1.5 \
        --delay 6 \
        --dir $dir \
        --period $period \
        --iperf $iperf \
        --burst 0.3 \
        --minRTO $minRTO \
        --tcp-n $tcp_n

      ./util/plot-rto.py --dir $dir --out $dir/result.png
    done
    ./util/plot.py --dir $rootdir/rto-$minRTO-tcp_n-$tcp_n/ --out $rootdir/rto-$minRTO-tcp_n-$tcp_n/result.png
  done
done
mycomment

#period=1
minRTO=900
tcp_n=1
for period in 1.1; do
  for burst in 0.30; do 
  dir=$rootdir/period-$period-tcp_n-$tcp_n/burst-$burst/
  
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
    --tcp-n $tcp_n 

  ./util/fourier-plot.py --dir $dir --out $dir/$period-$burst-result.png>/dev/null
  python ./util/plot_time_series.py --dir $dir --out $dir/$period-$burst-timeseries.png>/dev/null
  python ./util/plot_queue.py --maxy 100 --miny 0 -f $dir/qlen.txt -o $dir/queue.png >/dev/null
  python ./util/plot_tcpprobe.py -f $dir/tcp_probe.txt -o $dir/tcp_cwnd_iperf.png -p 5001 >/dev/null
  #mn -c
  done
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
