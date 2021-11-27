import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import sys
import constants
import socket
from aiclient import AIClient


if __name__ == "__main__":
    if len(sys.argv) < constants.NUM_CMD_ARG:
        print("Missing command line argument (role, timeout, server IP).")
        exit(-1)
    if sys.argv[1].lower() != constants.W_NAME and sys.argv[1].lower() != constants.B_NAME:
        print("You must specify which player you are (WHITE or BLACK)!")
        exit(-1)
    time = 60
    if len(sys.argv) > 2:
        time = sys.argv[2]
    ip = "localhost"
    if len(sys.argv) > 3:
        try:
            socket.inet_aton(sys.argv[3])
            ip = sys.argv[3]
        except:
            print("Invalid IP address format")
            exit(-1)


    # TODO: check instaurazione connessione
    client = AIClient(player=sys.argv[1].lower(), timeout=time, ipAddress=ip)
    client.run()

