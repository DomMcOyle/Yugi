from client import Client
import constants
import min_maxing
import traceback


class AIClient(Client):
    def __init__(self, player, name="Yugi", timeout=60, ipAddress="localhost"):
        super().__init__(player, name, timeout, ipAddress)

    def run(self):
        print("Chosen player: " + self.player)
        gm = min_maxing.tablut_game()
        try:
            self.declare_name()
            print(  """
                        ,------------.
                        (_\           \\
                          | Gioca la:  |
                          | partita    |
                          | Vinci la:  |
                          | fatica     |
                          | Questa è:  |
                          | la tua vita|
                         _| Yu-Gi-Oh.  |
                        (_/_____(*)___/
                                 \\
                                  ))
                    """)
        except:
            traceback.print_exc()
            self.sock.close()
            return

        if self.player == constants.W_PLAYER:
            opponent = constants.B_PLAYER
        else:
            opponent = constants.W_PLAYER

        try:
            depth = 2
            while True:
                self.read()
                print("Current state:")
                self.current_state.render()
                if self.get_current_state().get_current_player() == self.player:
                    print("DORO!")

                    # heurodance 2000 https://www.youtube.com/watch?v=jYjyoeHRMmc
                    move_to_do, alpha_comp_time = gm.alphabeta_search(self.get_current_state(), gm, self.player, d=depth)
                    print("time for an alpha evaluation: " + str(alpha_comp_time))
                    from_ = move_to_do[0]
                    to = move_to_do[1]
                    self.write(min_maxing.tablut_move.to_json_dict(from_, to, self.player))
                    if alpha_comp_time <= constants.TIME_THRESHOLD / 3:
                        depth += 1
                    else:
                        depth = 2
                    print("MONSTA KADO!")
                    # input move
                elif self.get_current_state().get_current_player() == opponent:
                    print("Waiting for the opponent's End Phase...")
                elif self.get_current_state().get_current_player() == constants.W_WIN:
                    print("WHITE WINS! - Black sent to the shadow realm...")
                    exit(1)
                elif self.get_current_state().get_current_player() == constants.B_WIN:
                    print("BLACK WINS! - White sent to the shadow realm...")
                    exit(1)
                elif  self.get_current_state().get_current_player() == constants.DRAW:
                    print("DRAW! - I activate SELF-DESTRUCT BUTTON!")
                    exit(1)
        except SystemExit:
            self.sock.close()
            return
        except:
            traceback.print_exc()
            self.sock.close()
            return

