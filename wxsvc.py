import json
from flask import Flask, request, render_template

app = Flask(__name__)
rc = 0

def incr(d):
  global rc
  rc += 1
  d['rc'] = rc


@app.route('/')
def root():
  return render_template('./home.html')

@app.route('/api/trans/a', methods=['POST'])
def svc():
  data = dict()
  incr(data)
  print(request.files)
  print(request)
  return json.dumps(data)
