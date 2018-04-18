from kalah import Kalah
from math import log, sqrt
import random
import copy

max_depth = 100
nodeDict  = {}
# wins      = {}
# players   = {}

def mcts_strategy(itermax):
    def fxn(pos):
        move = mcts(itermax, pos)
        return move
    return fxn

class Node:
    def __init__(self, move = None, state = None, parent = None, player = None):
        self.move         = move
        self.parentNode   = parent
        self.childrenList = []
        self.visitTimes   = 0
        self.winScore     = 0
        self.futureMoves  = state.legal_moves()
        self.nextPlayer   = player

    def UCTselection(self):
        total_visits = 0
        for c in self.childrenList:
            total_visits += c.visitTimes
        s = sorted(self.childrenList, key = lambda c: c.winScore/c.visitTimes + sqrt(2*log(total_visits)/c.visitTimes))[-1]
        s.parentNode = self
        return s
    
    def AddNode(self, m, s, posPlayer):
        if (posPlayer, s) in nodeDict:
            n.move = m
            n.parentNode = self    
            n = nodeDict[(posPlayer, s)]   
        else:
            n = Node(move = m, state = s, parent = self, player = posPlayer)
        nodeDict[(posPlayer, s)] = n

        self.futureMoves.remove(m)
        self.childrenList.append(n)
        return n
    
    def Update(self, result):
        self.visitTimes += 1
        self.winScore   += result

def mcts(itermax, pos):
    # check if initial state meet
    posPlayer = pos.next_player()
    if pos.is_initial():
        nodeDict.clear()
    # check the node dict    
    if (posPlayer, pos) in nodeDict:
        root = nodeDict[(posPlayer, pos)]
        root.parentNode = None
    else:
        root = Node(state = pos, player = posPlayer)
        nodeDict[(posPlayer, pos)] = root

    # do the iteration
    for i in range(itermax):
        node  = root
        state = copy.deepcopy(pos)
        posPlayer = pos.next_player()

        # Select
        while node.futureMoves == [] and node.childrenList != []:
            node      = node.UCTselection()
            print("state_before:", state.next_player())
            state     = state.result(node.move)
            print("state_afterb:", state.next_player())
            posPlayer = state.next_player()
        
        # Expand
        if node.futureMoves != []:
            rmchoice  = random.choice(node.futureMoves)
            state     = state.result(rmchoice)
            posPlayer = state.next_player()
            node      = node.AddNode(rmchoice, state, posPlayer)

        # Rollout
        while not state.game_over():
            state     = state.result(random.choice(state.legal_moves()))
            posPlayer = state.next_player()

        # Backpropagate
        curWinner = state.winner()
        while node != None:
            point = 0
            if (node.nextPlayer == 1 and curWinner == 1) or (node.nextPlayer == 0 and curWinner == -1):
                point += 1
            elif curWinner == 0:
                point += 0.5
            node.Update(point)
            node = node.parentNode
    
    return sorted(root.childrenList, key = lambda c: c.winScore/c.visitTimes)[-1].move

if __name__ == '__main__':
    b = Kalah(6)
    pos = Kalah.Position(b, [6, 4, 2, 0, 0, 2, 9, 0, 0, 2, 2, 6, 6, 9], 0)
    print(mcts_strategy(1000)(pos))
    '''
    pos = Kalah.Position(b, [0, 0, 2, 2, 6, 6, 9, 6, 4, 2, 0, 0, 2, 9], 1)
    print(mcts_strategy(1000)(pos))
    '''