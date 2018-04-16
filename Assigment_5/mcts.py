from kalah import Kalah
from math import *
import random

def mcts_strategy(itermax):
    def fxn(pos):
        move = mcts(itermax, pos)
        return move
    return fxn

class Node:
    def __init__(self, move = None, state = None, parent = None):
        self.move         = move
        self.parentNode   = parent
        self.childrenList = []
        self.visitTimes   = 0
        self.winScore     = 0
        self.futureMoves  = state.legal_moves()
        self.player       = state.next_player()

    def UCTselection(self):
        s = sorted(self.childrenList, key = lambda c: c.winScore/c.visitTimes + sqrt(2*log(self.visitTimes)/c.visitTimes))[-1]
        return s
    
    def AddNode(self, m, s):
        n = Node(move = m, state = s, parent = self)
        self.futureMoves.remove(m)
        self.childrenList.append(n)
        return n
    
    def Update(self, result):
        self.visitTimes += 1
        self.winScore += result

def mcts(itermax, pos):
    root = Node(state = pos)
    
    for i in range(itermax):
        node  = root
        state = pos
        
        # Select
        while node.futureMoves == [] and node.childrenList != []:
            node  = node.UCTselection()
            state = state.result(node.move)
       
        # Expand
        if node.futureMoves != []:
            rmchoice = random.choice(node.futureMoves)
            state    = state.result(rmchoice)
            node     = node.AddNode(rmchoice, state)
        
        # Rollout
        while state.game_over() == 0:
            state = state.result(random.choice(state.legal_moves()))

        # Backpropagate
        while node != None:
            point = 1 if node.player == state.winner() else 0
            node.Update(point)
            node = node.parentNode
    rs = sorted(root.childrenList, key = lambda c: c.visitTimes)[-1].move
    print(rs)
    return rs

