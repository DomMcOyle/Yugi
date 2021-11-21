import min_maxing
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
            opponent = constants.B_PLAYER
        else:
            opponent = constants.W_PLAYER

        try:
            while True:
                self.read()
                print("Current state:")
                self.current_state.render()
                if self.get_current_state().get_current_player() == self.player:
                    print("DORO!")
                    """
                    !!!INSERT HEURISTIC HERE !!!
                    """
                    from_ = input()
                    to = input()
                    self.write(min_maxing.tablut_move.to_json_dict(from_, to, self.player, convert=False))
                    # input move
                elif self.get_current_state().get_current_player() == opponent:
                    print("Waiting the opponent's End Phase...")
                elif self.get_current_state().get_current_player() == constants.W_WIN:
                    print("WHITE WINS! - Black sent to the shadow realm...")
                    exit(1)
                elif self.get_current_state().get_current_player() == constants.B_WIN:
                    print("BLACK WINS! - White sent to the shadow realm...")
                    exit(1)
                elif  self.get_current_state().get_current_player() == constants.B_WIN:
                    print("DRAW! - I activate SELF-DESTRUCT BUTTON!")
                    exit(1)
        except SystemExit:
            return
        except:
            traceback.print_exc()
            return