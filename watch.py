#!/home/pi/projects/sonos_dash/.venv/bin/python

from scapy.all import *
import json
import threading
import time

DATE = ""

if __name__ == '__main__':

  def arp_respond(pkt):
    if pkt[ARP].op == 1: # who-has (request)
      if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
        arp = pkt[ARP].hwsrc
        if arp_lookup.get(arp) in func_lookup:
          func_lookup[arp_lookup[arp]]()
          
  def sonos_toggle():
    print DATE

  with open('arp.json') as f:
    arp_lookup = json.load(f)

  func_lookup = {
    'loreal_dash': sonos_toggle
  }

  t = threading.Thread(target=sniff, kwargs={'prn': arp_respond, 'filter': 'arp', 'store': 0, 'count': 0})
  t.daemon = True
  t.start()

  while True:
    DATE = time.time()
    time.sleep(1)
