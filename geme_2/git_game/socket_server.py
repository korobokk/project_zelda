import socket
from server_connection import *


class Local_host(object):
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1', 2000))
        self.mydb = Database('localhost', 'root', '7568853Ar', 'testdb123')
        print(self.mydb.connection_status())

    def connection(self):
        self.server.listen()
        try:
            print('working..')
            client_s, address = self.server.accept()
            data = client_s.recv(1024).decode('utf-8')
            print(data)
            if self.check_valid_datapack(data):
                name, email, password, results = data.split(',')
                results = float(results)
                self.mydb.insert_user(name, email, password, results)
            if data == 'give_table':
                send = ''
                content = self.mydb.get_table()
                for name, result in content:
                    send += str(name) + ',' + str(int(result)) + ';'
                client_s.send(bytes(send[:-1], 'utf-8'))
            print('shutdown this shit...')
        except:
            print('Bad prompts... ')

    def check_valid_datapack(self, data):
        try:
            name, email, password, results = data.split(',')
            return True
        except:
            return False


server1 = Local_host()
while True:
    server1.connection()
