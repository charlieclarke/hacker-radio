import string
import os

from evdev import InputDevice
from select import select

dev = InputDevice('/dev/input/event1')

def numbers_to_keys(argument):
    switcher = {
        105: "left",
        103: "up",
        106: "right",
        108: "down",
        57: "space",
        272: "click",
    }
    return switcher.get(argument, "x")

def key_to_station(argument):
    switcher = {
        "left": "loadlist http://www.listenlive.eu/bbcradio4.m3u 0",
	"right": "loadlist http://www.listenlive.eu/rte1.m3u 0",
        "up": "loadlist http://broadcast.infomaniak.ch/jazz-wr04-128.mp3.m3u 0",
        "down": "loadlist http://uk1-pn.mixstream.net/8698.m3u 0",
        "space": "pause",
        "click": "pause",
    }
    return switcher.get(argument, "x")

fifo_write = open('/tmp/mplayer-control', 'w')

while True:
   r,w,x = select([dev], [], [])
   for event in dev.read():

        if event.type==1 and event.value==1:
                print "got input %s type %s value %s code %s" %(numbers_to_keys(event.code), event.type, event.value, event.code)
		mplayercmd = key_to_station(numbers_to_keys(event.code))
		print "mplayer command is %s", mplayercmd
		thecmd = 'echo "$mplayercmd" > /tmp/mplayer-control'
		print thecmd

		fifo_write.write(mplayercmd)
		fifo_write.write("\n")
		fifo_write.flush()



		


