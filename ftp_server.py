import multiprocessing
import os
import threading
import json

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from http_server import flask_run

try:
    with open('config.json', encoding='utf-8') as f:
        config = json.load(f)
except:
    config_s = \
'''{
    "port": 2121,
    "C_root_path": "C:\\\\",
    "D_root_path": "D:\\\\"
}
'''
    with open('config.json', 'w', encoding='utf-8') as f:
        f.write(config_s)
    with open('config.json', encoding='utf-8') as f:
        config = json.load(f)

def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user('C', '12345', config.get('C_root_path', 'C:\\'), perm='elradfmwMT')
    authorizer.add_user('D', '12345', config.get('D_root_path', 'D:\\'), perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready."

    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #handler.masquerade_address = '151.25.42.11'
    #handler.passive_ports = range(60000, 65535)

    # Instantiate FTP server class and listen on 0.0.0.0:2121
    address = ('0.0.0.0', config['port'])
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    threading.Thread(target=flask_run).start()
    main()