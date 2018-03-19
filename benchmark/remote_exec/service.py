from flask import Flask
from flask import request
import socket
import os
import sys
import requests
import json
import math
# import backend

app = Flask(__name__)

TRACE_HEADERS_TO_PROPAGATE = [
    'X-Ot-Span-Context',
    'X-Request-Id',
    'X-B3-TraceId',
    'X-B3-SpanId',
    'X-B3-ParentSpanId',
    'X-B3-Sampled',
    'X-B3-Flags'
]


def exec_str(func_str, func_name, func_param):
    # return ast.literal_eval(func_param)
    print(func_str)
    # print(func_name)
    param = func_param
    # print(param)
    # if param is list:
    #     param_str = '[' + ','.join(func_param) + ']'
    # else:
    #     param_str = param

    # print(param)
    exec(func_str)
    # r = eval(func_name + '({})'.format(param))
    # r = [eval(func_name + '({})'.format(i)) for i in param]
    r = []
    for p in param:
        r0 = eval(func_name + '({})'.format(p))
        r.append(r0)

    # print('param_str', param_str)
    # print('r', r)

    return r


@app.route('/service/<service_number>', methods=['GET', 'POST'])
def hello(service_number):
    # print(request.values)
    func_str = request.values.get('func_str', None)
    func_name = request.values.get('func_name', None)
    func_data = request.values.getlist('func_data', None)

    print('func_str', func_str)
    print('func_data', func_data)

    is_success = False
    func_result = None
    func_exception = None
    if func_str is not None and func_name is not None and func_data is not None:
        try:
            func_result = exec_str(func_str, func_name, func_data)
            # print(func_result)
            is_success = True
        except Exception as e:
            is_success = False
            func_exception = str(e)

    result = {
        # 'envoy': {
        #     'service_number': service_number,
        #     'service': os.environ['SERVICE_NAME'],
        #     'hostname_resolved': socket.gethostname(),
        #     'hostname': socket.gethostbyname(socket.gethostname())
        # },
        'data': request.values.get('echo', ''),
        'test': 'Hello test',
        'input': {
            'func_str': func_str,
            'func_name': func_name,
            'func_data': func_data
        },
        'function': {
            'success': is_success,
            'result': func_result if func_result is not None else '',
            'exception': func_exception if func_exception is not None else ''
        } if func_str is not None and func_name is not None and func_data is not None else {}
    }

    return json.dumps(result)

    # return ('Hello from behind Envoy (service {})! hostname: {} resolved'
    #         'hostname: {}\n'.format(os.environ['SERVICE_NAME'],
    #                                 socket.gethostname(),
    #                                 socket.gethostbyname(socket.gethostname())))


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

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=5000, debug=True)
