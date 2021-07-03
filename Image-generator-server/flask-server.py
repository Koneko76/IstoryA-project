from flask import Flask
from flask import request
import os
import sys
app = Flask(__name__)

@app.route('/')
def ping():
    return 'OK!'

@app.route('/picture_generation', methods=['GET', 'POST'])
def generate_picture():

    print(str(request.args.get('text')))

    os.spawnl(os.P_NOWAIT,
              sys.executable,
              sys.executable, "picture-generation.py",
              '"' + str(request.args.get('text')) + '"',
              str(request.args.get('storyboard_id')),
              str(request.args.get('case_id')),
              str(request.args.get('owner_id')))

    return 'OK'
