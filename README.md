# Yugi
AI player for Tablut Challenge 21/22@Unibo

## How it works
The player consists in:
- An implementation of bounded minimax with alpha/beta pruning algorithm.
  - The algorithm stops the in-depth search if the maximum depth, a final state or a time bound has been reached.
  - The initial maximum depth is 2 and it is increased if in the previous search the algorithm employed less than a third of the time bound.
- The heuristic applied consists in a "manual" heuristic which considers common indicators of the quality of the state (number of pawns, particular positions...) which is weighted by the value returned from a neural network (Atem) trained on a given dataset (further information on the network structure and on the dataset can be found in <code>info.txt</code> in the respective folders)
  - The neural network has been trained using a hyper-parameter tuning framework [hyperas](https://github.com/maxpumperla/hyperas). The search space given was composed of commonly used values for training.

## Starting the player
The player can be started by typing in the command line, while in /tablut:
<br><code>python3 DPGR.py role [timeout] [ip_address]</code><br>

- <code>role</code> is the only mandatory argument, must be either "BLACK" or "WHITE"
	(not case sensitive). It indicates which role the AI plays.
- <code>timeout</code> integer representing the timeout set for the move. If not
	given, assumes 60 as default.
- <code>ip_address</code> string indicating the IP address of the server. If not
	given, assumes "localhost" as default

also, the player can be started by launching the <code>runmyplayer</code> bash script in the virtual machine:
<br><code>./runmyplayer role [timeout] [ip_address]</code><br>
with the same argument as the previous
  
## Training
If needed, the training script can be launched as follows:
<br><code>python3 training.py action name</code><br>
- <code>action</code> can be either 'train' or 'test'. In the first case, the script is launched to train a new network on <code>parsed_dataset_v3.csv</code> with hyperparameter optimization. In the latter case, the given net is tested on the whole dataset.
- <code>name</code> is the argument containing the name of the net to train/use

## Quick start commands for playing on the same machine
 - Playing as white:
   <br><code>python3 DPGR.py 'WHITE'</code>
   <br><code>./runmyplayer 'WHITE'</code>
 - Playing as black:
   <br><code>python3 DPGR.py 'BLACK'</code>
   <br><code>./runmyplayer 'BLACK'</code>
