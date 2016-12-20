echo 'in launcher' >> /var/tmp/launcher
echo `date` >> /var/tmp/launcher

pkill mplayer
rm /tmp/mplayer-control
mkfifo /tmp/mplayer-control


echo 'start pinger' >> /var/tmp/launcher
while : 
do

    echo 'ping' >> /var/tmp/launcher
    if /home/chip/ping.sh www.google.com 
    then
        break
    fi
done

echo 'done pinger' >> /var/tmp/launcher

nohup /usr/bin/mplayer  -slave -input file=/tmp/mplayer-control -playlist http://www.listenlive.eu/bbcradio4.m3u &
echo 'done launch mplayer' >> /var/tmp/launcher
nohup python /home/chip/slider.py &
echo 'done' >> /var/tmp/launcher
 
