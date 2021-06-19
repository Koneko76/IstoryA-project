from flask import Flask
from flask import request
import os
import sys
app = Flask(__name__)

@app.route('/')
def hello_world():
    print("coucou2")
    return 'Hello, World!'

@app.route('/picture_generation', methods=['GET', 'POST'])
def hello():

    print("coucou", str(request.args.get('text')))

    os.spawnl(os.P_NOWAIT,
              sys.executable,
              sys.executable, "picture-generation.py",
              '"' + str(request.args.get('text')) + '"',
              str(request.args.get('storyboard_id')),
              str(request.args.get('case_id')),
              str(request.args.get('owner_id')))

    return 'Hello, CC'