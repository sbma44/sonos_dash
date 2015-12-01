#!/home/pi/projects/sonos_dash/.venv/bin/python

import sys
import soco
import logging
import os
import json
import threading
import time
import datetime
import settings
from scapy.all import *

logging.basicConfig(format='[sonos_dash] [%(levelname)s] %(message)s', level=logging.WARN)
LOGGER = logging.getLogger('sonos_dash')

SONOS = {}
DEFAULT_VOLUME = {
    'Kitchen': 60
}

if __name__ == '__main__':
  LOGGER.warn('starting')

  def arp_respond(pkt):
    if pkt.haslayer(ARP):
      if pkt[ARP].op == 1: # who-has (request)
        if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
          arp = pkt[ARP].hwsrc
          if arp_lookup.get(arp) in func_lookup:
            func_lookup[arp_lookup[arp]]()
          
  def sonos_toggle_kitchen():
    LOGGER.warn('firing sonos_toggle_kitchen()')

    sonos = SONOS.get('Kitchen', False)
    if not sonos:
      LOGGER.error('no sonos available')
      return

    if sonos.get_current_transport_info().get('current_transport_state') == 'PLAYING':
      sonos.stop()
    else:
      wamu = settings.WAMU_URI
      wbez = settings.WBEZ_URI
      music = settings.get_music_uri()

      now = datetime.datetime.now()

      # old time radio - sunday between 6:45 and 11pm
      if now.isoweekday() == 7 and now.hour < 23 and ((now.hour * 60) + now.minute) > 1125:
        sonos.play_uri(wamu)
        return

      # morning (early)
      if now.hour < 11:
        if now.hour >= 9 and now.hour < 10:
          sonos.play_uri(wbez)
        else:
          sonos.play_uri(wamu)
        return

      # evening in general
      sonos.play_uri(music)

  with open('{}/arp.json'.format(settings.DIRECTORY)) as f:
    arp_lookup = json.load(f)

  func_lookup = {
    'loreal_dash': sonos_toggle_kitchen
  }

  LOGGER.warn('starting ARP sniffer')
  t = threading.Thread(target=sniff, kwargs={'prn': arp_respond, 'filter': 'arp', 'store': 0, 'count': 0})
  t.daemon = True
  t.start()

  while True:
    sd = soco.discover()
    if sd is not None and len(sd) > 0:
      for m in sd:
        if not m.player_name in SONOS:
          LOGGER.warn('found new sonos: {}'.format(m.player_name))
          SONOS[m.player_name] = m
    time.sleep(30)

