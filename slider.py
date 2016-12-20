import string
import os
import csv


from evdev import InputDevice
from select import select


voltage = '/sys/bus/iio/devices/iio:device0/in_voltage0_raw'

minv = 0
maxv = 60 

station_list = []

with open('/home/chip/stations.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile)
	for row in spamreader:
		if (len(row)==2):
			station_list.append(row)
			print 'station' + row[0] + '-' + row[1]


fifo_write = open('/tmp/mplayer-control', 'w')

def get_voltage():

	tfile = open(voltage) 
	try:
		text = tfile.read() 
	except IOError:
		text=str(maxv)
	
	tfile.close() 

	return int(text)

def calc_station(maxv, voltage, scale):
	station_p = float(voltage)/float(maxv) * scale

	return int(station_p)

current_voltage = get_voltage()
current_station = calc_station(maxv, current_voltage, len(station_list)-1)

station_url = station_list[current_station][0]
station_name = station_list[current_station][1]
fifo_write.write( 'loadlist' + ' ' + station_url)
fifo_write.write("\n")
fifo_write.flush()
while True:

	new_voltage = get_voltage()

	if (new_voltage <> current_voltage):
		print "new voltage is" + str(new_voltage)
		new_station = calc_station(maxv, new_voltage, len(station_list)-1) 

		if (new_station <> current_station):

			station_url = station_list[new_station][0]
			station_name = station_list[new_station][1]

			print "volt of " + str(new_voltage)  + " so changing to " + station_name + "|" + station_url 


			print "mplayer command is %s",station_url 

			thecmd = 'echo loadlist "$station_name" > /tmp/mplayer-control'
			print thecmd

			fifo_write.write( 'loadlist' + ' ' + station_url)
			fifo_write.write("\n")
			fifo_write.flush()



			current_station = new_station

	current_voltage = new_voltage
'''
        if event.type==1 and event.value==1:
                print "got input %s type %s value %s code %s" %(numbers_to_keys(event.code), event.type, event.value, event.code)
		mplayercmd = key_to_station(numbers_to_keys(event.code))
		print "mplayer command is %s", mplayercmd
		thecmd = 'echo "$mplayercmd" > /tmp/mplayer-control'
		print thecmd

		fifo_write.write(mplayercmd)
		fifo_write.write("\n")
		fifo_write.flush()
'''


		


