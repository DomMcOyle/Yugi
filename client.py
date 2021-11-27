import socket
import json

import constants
import min_maxing


class Client():
    def __init__(self, player, name="Yugi", timeout=60, ipAddress="localhost"):
        self.serverIp = ipAddress
        self.timeout = timeout
        if timeout - constants.TIME_MARGIN > constants.TIME_MARGIN:
            constants.TIME_THRESHOLD = timeout - constants.TIME_MARGIN
        else:
            constants.TIME_THRESHOLD = timeout - 3 # 3 seconds for luck, magic number
        if player.lower() == constants.B_NAME:
            self.player = constants.B_PLAYER
            self.port = constants.B_PORT
        elif player.lower() == constants.W_NAME:
            self.port = constants.W_PORT
            self.player = constants.W_PLAYER
        else:
            raise ValueError("Player role must be BLACK or WHITE")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.serverIp, self.port))
        self.name = name

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def write(self, action):
        #action will be a dictionary
        jfiglio = json.dumps(action) + '\r\n'
        j_byte = jfiglio.encode('utf-8')
        self.sock.sendall(len(j_byte).to_bytes(4,'big'))
        self.sock.sendall(j_byte)

    def declare_name(self):
        send_name = self.name + '\r\n'
        name_b = send_name.encode('utf-8')
        self.sock.sendall(len(name_b).to_bytes(4,'big'))
        self.sock.sendall(name_b)

    def read(self):
        l = b''
        while len(l) < 4:
            data = self.sock.recv(4-len(l))
            if data:
                l += data
        l = int.from_bytes(l,'big')
        recieved = b''
        while len(recieved)<l:
            data = self.sock.recv(l-len(recieved))
            if data:
                recieved += data
        self.current_state = min_maxing.tablut_state.from_json_dict_state(json.loads(recieved.decode(encoding='utf-8')))

    def get_player(self):
        return self.player

    def set_player(self, pl):
        self.player = pl

    def set_current_state(self, state):
        self.current_state = state

    def get_current_state(self):
        return self.current_state
