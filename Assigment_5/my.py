from math import log, sqrt
import random

max_depth = 100

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
        self.winScore   += result

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
        simuDepth = 0
        while not state.game_over() and simuDepth < max_depth:
            simuDepth += 1
            state = state.result(random.choice(state.legal_moves()))

        # Backpropagate
        terminal_state = state.game_over()
        curWinner = state.winner()
        while node != None:
            point = 0
            if terminal_state and (node.player == 0 and curWinner == 1) or (node.player == 1 and curWinner == -1):
                point += 1
            node.Update(point)
            node = node.parentNode

    return sorted(root.childrenList, key = lambda c: c.visitTimes)[-1].move

