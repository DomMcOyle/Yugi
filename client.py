import socket
import json

import constants


class Client():
    def __init__(self, player, name="Yugi", timeout=60, ipAddress="localhost"):
        self.serverIp = ipAddress
        self.timeout = timeout
        if player.lower() == constants.B_NAME:
            self.player = constants.B_PLAYER
            self.port = constants.B_PORT
        elif player.lower() == constants.W_NAME:
            self.port = constants.W_PORT
            self.player = constants.W_PLAYER
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

    def get_player(self):
        return self.player

    def set_player(self, pl):
        self.player = pl

    def set_current_state(self, state):
        self.state = state

    def get_current_state(self):
        return self.state
