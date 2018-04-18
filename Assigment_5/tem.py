from kalah import Kalah
from math import log, sqrt
import random
import copy

nodeDict  = {}

def mcts_strategy(itermax):
    def fxn(pos):
        move = mcts(itermax, pos)
        return move
    return fxn

class Node:
    def __init__(self):
        self.visitTimes = 0
        self.winScore   = 0

def UCTselection(player, reslist):
    total_visits = 0
    for move, res in reslist:
        total_visits += nodeDict.get((player, res)).visitTimes
    '''
    uctValues = list()
    for move, cRes in reslist:
        node  = nodeDict.get((player, cRes))
        value = node.winScore / node.visitTimes + sqrt(2*log(total_visits) / node.visitTimes) 
        uctValues.append((value, move))
    return_res = sorted(uctValues, key = lambda x:x[0])[-1][1]
    print("Select:", repr(return_res))
    '''
    return_res = None
    best_value = -float('inf')
    for move, cRes in reslist:
        node  = nodeDict.get((player, cRes))
        value = node.winScore / node.visitTimes + sqrt(2*log(total_visits) / node.visitTimes) 
        if value > best_value:
            best_value = value
            return_res = cRes
    #print("Select:", repr(return_res))
    return return_res

def mcts_helper(pos):
    # state = copy.deepcopy(pos)
    posPlayer = pos.next_player()
    visit_path = set()
    expand = True
    curWinner = None
   
    while True:
        cur_res = []
        for move in pos.legal_moves():
            cur_res.append((move, pos.result(move)))
        #print(len(cur_res))
        if all(nodeDict.get((posPlayer, cRes)) for move, cRes in cur_res):
            next_state = UCTselection(posPlayer, cur_res)
        else:
            useless, next_state = random.choice(cur_res)
        
        if expand:
            visit_path.add((posPlayer, next_state))
        # if need to expand
        if expand and (posPlayer, next_state) not in nodeDict:
            expand = False
            new_node = Node()
            nodeDict[(posPlayer, next_state)] = new_node
        #print("before: ", repr(pos))
        pos = next_state
        #print("after: ", repr(pos))
        posPlayer = pos.next_player()
        if pos.game_over():
            curWinner = pos.winner()
            break
    # Backpropagate
    for player_, state_ in visit_path:
        if (player_, state_) in nodeDict:
            nodeDict[(player_, state_)].visitTimes += 1
            if (posPlayer == 0 and curWinner == 1) or (posPlayer == 1 and curWinner == -1):
                nodeDict[(player_, state_)].winScore += 1

def mcts(itermax, input_pos):
    # check if termianl state
    if input_pos.game_over():
        return
    if len(input_pos.legal_moves()) == 1:
        return input_pos.legal_moves()[0]
    # check if initial 
    if input_pos.is_initial():
        nodeDict.clear()

    # do the iteration
    for i in range(itermax):
        mcts_helper(input_pos)

    posPlayer = input_pos.next_player()
    '''
    reslist = list()
    for move in input_pos.legal_moves():
        res_state = input_pos.result(move)
        if (posPlayer, res_state) in nodeDict:
            thenode = nodeDict[(posPlayer, res_state)]
            reslist.append((thenode.winScore / thenode.visitTimes, move))
        else:
            reslist.append((0, move))

    return sorted(reslist, key = lambda x:x[0])[-1][1]
    '''
    best_move = None
    best_value = -float('inf')
    for move in input_pos.legal_moves():
        res_state = input_pos.result(move)
        cvalue = 0
        if (posPlayer, res_state) in nodeDict:
            thenode = nodeDict[(posPlayer, res_state)]
            cvalue  = thenode.winScore / thenode.visitTimes
        if cvalue > best_value:
            best_value = cvalue
            best_move  = move
    return best_move

if __name__ == '__main__':
    b = Kalah(6)
    pos = Kalah.Position(b, [6, 4, 2, 0, 0, 2, 9, 0, 0, 2, 2, 6, 6, 9], 0)
    print(mcts_strategy(1000)(pos))

    pos = Kalah.Position(b, [0, 0, 2, 2, 6, 6, 9, 6, 4, 2, 0, 0, 2, 9], 1)
    print(mcts_strategy(1000)(pos))