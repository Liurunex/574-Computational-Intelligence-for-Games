from kalah import Kalah
from math import log, sqrt
import random
import copy

max_depth = 100
nodeDict  = {}
wins      = {}
players   = {}

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
        self.nextPlayer   = state.next_player()

    def UCTselection(self, state):
        s = sorted(self.childrenList, key = lambda c: c.winScore/c.visitTimes + sqrt(2*log(self.visitTimes)/c.visitTimes))[-1]
        s.parentNode = self
        return s
    
    def AddNode(self, m, s):
        if s in nodeDict:
            n      = nodeDict[s]
            n.move = m
            n.parentNode = self    
        else:
            n = Node(move = m, state = s, parent = self)
        nodeDict[s] = n

        self.futureMoves.remove(m)
        self.childrenList.append(n)
        return n
    
    def Update(self, result):
        self.visitTimes += 1
        self.winScore   += result

def mcts(itermax, pos):
    # check if initial state meet
    if pos.is_initial():
        nodeDict.clear()
    # check the node dict    
    if pos in nodeDict:
        root = nodeDict[pos]
        root.parentNode = None
    else:
        root = Node(state = pos)
        nodeDict[pos] = root

    # do the iteration
    for i in range(itermax):
        node  = root
        state = copy.deepcopy(pos)
        
        vistied_node = set()

        # Select
        while node.futureMoves == [] and node.childrenList != []:
            node  = node.UCTselection(state)
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
            point = 1
            if terminal_state and (node.nextPlayer == 0 and curWinner == 1) or (node.nextPlayer == 1 and curWinner == -1):
                point -= 1
            elif curWinner == 0:
                point -= 0.5
            node.Update(point)
            node = node.parentNode
    return sorted(root.childrenList, key = lambda c: c.winScore/c.visitTimes)[-1].move

if __name__ == '__main__':
    b = Kalah(6)
    pos = Kalah.Position(b, [6, 4, 2, 0, 0, 2, 9, 0, 0, 2, 2, 6, 6, 9], 0)
    print(mcts_strategy(1000)(pos))

    pos = Kalah.Position(b, [0, 0, 2, 2, 6, 6, 9, 6, 4, 2, 0, 0, 2, 9], 1)
    print(mcts_strategy(1000)(pos))