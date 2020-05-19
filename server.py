import os
import time

import socketio

from file import FileManage

# create a Socket.IO server
sio = socketio.Server(async_mode='gevent')

# wrap with a WSGI application
app = socketio.WSGIApp(sio)

file = FileManage(current_dir='C:\\')

current_file_path= ''

def update_server_display():
    sio.emit('server_dir_files', [
        file.sub_directory_list,
        file.sub_file_list,
        file.current_dir
    ])

@sio.event
def test(sid, data):
    print(type(data))
    pass

@sio.event
def send_file(sid, data):
    """

    :param sid:
    :param file_path:
    :return:
    """
    server_dir = data['server_dir']
    filename = data['filename']
    start_position = data['start_position']
    length = data['length']
    with open(os.path.join(server_dir, filename), 'rb') as f:
        f.seek(start_position)
        part = f.read(length)
        sio.emit('receive_file', part)

@sio.event
def receive_file_request(sid, data):
    global current_file_path
    current_file_path = data
    sio.emit('send_file', '')

@sio.event
def receive_file(sid, data):
    if data:
        try:
            f = open(current_file_path, 'ab')
            f.write(data)
            f.close()
        except PermissionError as e:
            print('PermissionError')
            time.sleep(0.5)
            pass
        else:
            pass
        finally:
            sio.emit('send_file', '')
    else:
        print('done')


@sio.event
def server_dir_files(sid, data):
    update_server_display()

@sio.event
def server_enter(sid, data):
    file.enter_from_current(data)
    update_server_display()

@sio.event
def server_enter_parent(sid, data):
    file.enter_parent()
    update_server_display()

@sio.event
def connect(sid, environ):
    update_server_display()
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

from gevent import pywsgi
pywsgi.WSGIServer(('', 5001), app).serve_forever()