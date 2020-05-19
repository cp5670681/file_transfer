from flask import Flask, jsonify, request
from utils.command import Command

app = Flask(__name__)


@app.route('/')
def test():
    return 'test'

@app.route('/process_list')
def process_list():
    return jsonify(Command.tasklist())

@app.route('/kill_process/<name>')
def kill_process(name):
    try:
        Command.kill_process(name)
        return '成功关闭程序{}'.format(name)
    except Exception as e:
        return str(e)

@app.route('/open_process', methods=['POST'])
def open_process():
    try:
        path = request.get_json().get('path')
        name = path.split('\\')[-1]
        Command.open_process(path)
        return '成功打开程序{}'.format(name)
    except Exception as e:
        return str(e)


def flask_run():
    app.run(port=5001, host='0.0.0.0')