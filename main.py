import sys
import constants
import socket
from aiclient import AIClient

if __name__ == "__main__":
    if len(sys.argv) < constants.NUM_CMD_ARG:
        print("Missing command line argument (role, timeout, server IP).")
        exit(-1)
    if sys.argv[0].lower() != constants.W_NAME and sys.argv[0].lower() != constants.B_NAME:
        print("You must specify which player you are (WHITE or BLACK)!")
        exit(-1)
    time = 60
    if len(sys.argv)>1:
        time = sys.argv[1]
    ip = "localhost"
    if len(sys.argv)>2:
        try:
            socket.inet_aton(sys.argv[2])
            ip = sys.argv[2]
        except:
            print("Invalid IP address format")
            exit(-1)


    # TODO: check instaurazione connessione
    client = AIClient(player=sys.argv[0], timeout=time, ipAddress=ip)
    client.run()

