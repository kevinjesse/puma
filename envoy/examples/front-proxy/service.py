from flask import Flask
from flask import request
from flask import render_template
import socket
import os
import sys
import requests
#from models import db, name

#app specific
#home = os.path.expanduser("/home/ubuntu")
#sys.path.append('/home/ubuntu/chatbox/backend/')
sys.path.insert(0, "/home/ubuntu/chatbox/backend")
import dialogueCtrl as dctrl
import uuid
import json


app = Flask(__name__)

# POSTGRES = {
#     'user': 'postgres',
#     'pw': '2251',
#     'db': 'postgres',
#     'host': 'localhost',
#     'port': '5432',
# }
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
# %(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)


TRACE_HEADERS_TO_PROPAGATE = [
    'X-Ot-Span-Context',
    'X-Request-Id',
    'X-B3-TraceId',
    'X-B3-SpanId',
    'X-B3-ParentSpanId',
    'X-B3-Sampled',
    'X-B3-Flags'
]


@app.route('/service/<service_number>', methods=['POST'])
#@app.route('/service/<service_number>')
def hello(service_number):
    #return "OFFLINE"
    #app specific html container
    _text = request.form['chatText']
    _mode = request.form['mode']
    _id = str(request.form['UUID'])

    if _id == '-1':
        _id = str(uuid.uuid4())

    #app specific python container
    response, userid, passiveLen, signal = dctrl.dialogueCtrl(json.dumps({'text':_text, 'mode':_mode,'id':_id}))
    # if response == dctrl.end_dialogue:
    #     signal = 'end'
    if signal != "listen":
        dctrl.dialogueIdle(userid, debug=True)
    return json.dumps({'response':response, 'userid': userid, 'signal':signal, 'passiveLen':passiveLen})
    #return ('hi')


@app.route('/trace/<service_number>')
def trace(service_number):
    headers = {}
    # call service 2 from service 1
    if int(os.environ['SERVICE_NAME']) == 1 :
        for header in TRACE_HEADERS_TO_PROPAGATE:
            if header in request.headers:
                headers[header] = request.headers[header]
        ret = requests.get("http://localhost:9000/trace/2", headers=headers)
    return ('Hello from behind Envoy (service {})! hostname: {} resolved'
            'hostname: {}\n'.format(os.environ['SERVICE_NAME'], 
                                    socket.gethostname(),
                                    socket.gethostbyname(socket.gethostname())))


@app.route('/')
def main():


    # peter = name.query.filter_by(primaryname='Keanu Reeves').first()
    # print peter.primaryname
    # print peter.birthyear

    return render_template('chatbox.html')

if __name__ == "__main__":
    dctrl.initResources()
    app.run(host='0.0.0.0', port=8080, debug=True)