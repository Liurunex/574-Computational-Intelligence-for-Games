import random
import math

wins  = {}
plays = {}
max_moves = 100

def mcts_strategy(itermax):
    def fxn(pos):
        move = mcts(itermax, pos)
        return move
    return fxn

def run_simulation(pos):
	childrenList = pos.legal_moves()
	randomChoice = random.choice(childrenList)
	state = pos.result(pos)
	
	pass

def mcts(itermax, pos):
	if pos.is_initial():
		wins.clear()
		plays.clear()
	
	for i in range(itermax):
		run_simulation(pos)
	pass
