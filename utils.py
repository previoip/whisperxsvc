import os
import requests
from subprocess import Popen

def download(d):
  if not os.path.exists(d['path']):
    os.makedirs(os.path.dirname(d['path']), exist_ok=True)
    Popen(['curl', '-L', d['url'], '--output', d['path']]).wait()
