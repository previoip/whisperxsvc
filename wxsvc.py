import logging
import json
from os import makedirs, remove as rm
from io import BytesIO
from tempfile import mkstemp
from time import time
from flask import Flask, request, render_template
from whisperx import load_audio
from wxloader import transcribe


CACHE_DIR = './cache/atemp'

app = Flask(__name__)
rc = 0
logger = logging.getLogger()
makedirs(CACHE_DIR, exist_ok=True)


def incr(d):
  global rc
  rc += 1
  d['rc'] = rc
  d['ts'] = time()


@app.route('/')
def root():
  return render_template('./home.html')


@app.route('/api/trans/a', methods=['POST'])
def svc():
  resp = dict()
  incr(resp)
  file = request.files.get('file', None)
  if file is None:
    logger.error('file recv is null')
    return {}

  fd, path = mkstemp(dir=CACHE_DIR)
  with open(fd, 'wb') as fp:
    fp.write(file.read())
  audio = load_audio(path)
  rm(path)
  resp['trans'] = list()
  resp['trans'].append(transcribe('ja', audio))
  # resp['trans'].append(transcribe('en', audio))
  print(resp['trans'])
  return json.dumps(resp)
