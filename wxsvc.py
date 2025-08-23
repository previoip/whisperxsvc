import json
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def root():
  return render_template('./home.html')

@app.route('/t', methods=['POST'])
def svc():
  data = dict()
  print(request.data)
  return json.dump(data)
