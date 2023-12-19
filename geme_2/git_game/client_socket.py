import socket


class Connection(object):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def get_connect(self):
        try:
            self.client.connect((self.ip, self.port))
        except:
            print('Error')

    def send_data(self, data):
        try:
            name, email, password, results = data
            send = name + ',' + email + ',' + password + ',' + results
            self.client.send(bytes(send, 'utf-8'))
        except:
            print('Error')

    def get_table(self):
        send = 'give_table'
        self.client.send(bytes(send, 'utf-8'))
        recieved_data = self.client.recv(1024)
        return recieved_data


