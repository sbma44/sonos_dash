DEFAULT_VOLUME = {
  'Kitchen': 59
}

WAMU_URI = 'aac://wamu-1.streamguys.com/wamu-1.aac'
WBEZ_URI = 'x-rincon-mp3radio://stream.wbez.org/wbez128.mp3'

def get_music_uri():
  return 'x-sonosprog-http:station-song%3a1766073%2f23050781.mp4?sid=29&flags=8224&sn=2'
