import logging
import json
from io import BytesIO
from flask import Flask, request, render_template
from whisperx import load_audio

AUDIO_CACHE_PATH = './cache/0'

app = Flask(__name__)
rc = 0
logger = logging.getLogger()

print(dir(request))

def incr(d):
  global rc
  rc += 1
  d['rc'] = rc


@app.route('/')
def root():
  return render_template('./home.html')

@app.route('/api/trans/a', methods=['POST'])
def svc():
  resp = dict()
  file = request.files.get('file', None)
  if file is None:
    logger.error('file recv is null')
    return {}
  with open(AUDIO_CACHE_PATH, 'wb') as fp:
    fp.write(file.read())
  audio = load_audio(AUDIO_CACHE_PATH)
  ...
  incr(resp)
  return json.dumps(resp)
