from client import Client
import traceback
import constants
import time

class AIClient(Client):
    def __init__(self, player, name="Yugi", timeout=60, ipAddress="localhost"):
        super().__init__(player, name, timeout, ipAddress)

    def run(self):
        print("Chosen player: " + self.player)
        try:
            self.declare_name()
        except:
            traceback.print_exc()
            return

        if self.player == constants.W_PLAYER:
            try:
                self.read()
                print("Current state:")
                print(self.get_current_state())
            except:
                traceback.print_exc()
                return
        else:
            try:
                self.read()
                print("Current state:")
                print(self.get_current_state())
            except:
                traceback.print_exc()
                return