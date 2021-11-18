import socket
import sys
import json

import constants

class client():
    def __init__(self, player, name="Yugi", timeout=60, ipAddress="localhost"):
        self.serverIp = ipAddress
        self.timeout = timeout
        if player.lower() == constants.b_name:
            self.player = constants.b_player
            self.port = constants.b_port
        elif player.lower() == constants.w_name:
            self.port = constants.w_port
            self.player = constants.w_player
        else:
            raise ValueError("Player role must be BLACK or WHITE")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.serverIp, self.port))
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def write(self, action):
        #action will be a dictionary
        jfiglio = json.dumps(action)
        j_byte = jfiglio.encode('utf-8')
        self.sock.send(len(j_byte).to_bytes(8,'big'))
        self.sock.send(j_byte)

    def declare_name(self):
        name_b = self.name.encode('utf-8')
        self.sock.send(len(name_b).to_bytes(8,'big'))
        self.sock.send(name_b)
        
    def read(self):
        len = int(self.sock.recv(8))
        recieved = self.sock.recv(len)
        self.current_state = json.loads(recieved.decode(encoding='utf-8'))


"""current_client = client("WHITE")
current_client.declare_name()
print(current_client.read())"""