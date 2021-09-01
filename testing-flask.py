import os
from flask_ngrok import run_with_ngrok
from flask import Flask, render_template

app = Flask(__name__)
run_with_ngrok(app)

@app.route('/',methods = ['POST'])
def hello_world():
  return 'Hello, World'

if __name__ == '__main__':
  app.run()