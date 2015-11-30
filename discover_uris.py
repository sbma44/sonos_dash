import soco
import time
import json

stations = {}
s = soco.SoCo('192.168.1.138')
with open('stations.json') as f:
  stations = json.load(f)

while True:
  info = s.get_current_track_info()
  if info['uri'] not in stations:
    print('Found new station: {} / {}'.format(info['title'], info['uri']))
    stations[info['uri']] = info
    with open('stations.json', 'w') as f:
      json.dump(stations, f, indent=4)
  time.sleep(1)
