import logging
import json
from os import makedirs, remove as rm
from io import BytesIO
from tempfile import mkstemp
from datetime import datetime
from threading import Lock
from flask import Flask, request, render_template
from whisperx import load_audio
from wxloader import transcribe


CACHE_DIR = './cache/atemp'

rc = 0
app = Flask(__name__)
logger = logging.getLogger(__name__)
svc_lock = Lock()
makedirs(CACHE_DIR, exist_ok=True)


def incr(d):
  global rc
  rc += 1
  d['rc'] = rc


def format_timerange(timestamp, start, end):
  r = '['
  r += datetime.fromtimestamp(timestamp/1000 + start).strftime("%H:%M:%S")
  r += '-'
  r += datetime.fromtimestamp(timestamp/1000 + end).strftime("%H:%M:%S")
  r += ']'
  return r


@app.route('/')
def root():
  return render_template('./home.html')

@app.route('/api/trans/a', methods=['POST'])
def svc():
  svc_lock.acquire(blocking=True)
  resp = dict()
  incr(resp)
  file = request.files.get('file', None)
  timestamp = float(request.form['ts'])
  if file is None:
    logger.error('file is null')
    return {}
  fd, path = mkstemp(dir=CACHE_DIR)
  with open(fd, 'wb') as fp:
    b = file.read()
    if len(b) == 0:
      logger.warning('lmfao blob contains no data try again')
      svc_lock.release()
      return resp
    fp.write(b)
  try:
    audio = load_audio(path)
    rm(path)
    resp['trans'] = list()
    resp['trans'].append(transcribe('ja', audio))
    # resp['trans'].append(transcribe('en', audio))
    for trans in resp['trans']:
      for seg in trans['segments']:
        seg['ts'] = format_timerange(timestamp, seg['start'], seg['end'])
  except Exception as e:
    logger.error(e)
  svc_lock.release()
  return json.dumps(resp)
