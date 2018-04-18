from kalah import Kalah
from math import sqrt, log
from random import choice

# dict used for DAG
# key = (player, res)
# value = [visits, wins]
nodeDict = {}

def mcts(pos):
    player = pos.next_player()
    expand = True
    visit_path = set()

    while True:
        cur_res = [pos.result(move) for move in pos.legal_moves()]
        if all(nodeDict.get((player, res)) for res in cur_res):
            total_visits = 0
            for cres in cur_res:
                total_visits += nodeDict.get((player, cres))[0]
            # UCB process:
            next_state = None
            best_value = -float('inf')
            for res in cur_res:
                node = nodeDict.get((player, res))
                value = node[1] / node[0] + sqrt(2*log(total_visits) / node[0])
                if value > best_value:
                    best_value = value
                    next_state = res
        else:
            next_state = choice(cur_res)

        # if need to expand
        if expand:
            visit_path.add((player, next_state))
        if expand and (player, next_state) not in nodeDict:
            expand = False
            nodeDict[(player, next_state)] = [0, 0]

        # Update
        pos = next_state
        player = pos.next_player()
        if pos.game_over():
            curWinner = next_state.winner()
            break

    # Back-propagate
    for player, pos in visit_path:
        if (player, pos) in nodeDict:
            nodeDict[(player, pos)][0] += 1
            if (player == 0 and curWinner == 1) or (player == 1 and curWinner == -1):
                nodeDict[(player, pos)][1] += 1


def mcts_strategy(itermax):
    def fxn(pos):
        # check if termianl state
        if pos.game_over():
            return None
        if len(pos.legal_moves()) == 1:
            return pos.legal_moves()[0]
        # check if initial
        if pos.is_initial():
            nodeDict.clear()

        for i in range(itermax):
            mcts(pos)

        posPlayer = pos.next_player()
        reslist = list()
        for move in pos.legal_moves():
            res = pos.result(move)
            value = nodeDict.get((posPlayer, res), [0, 0])[1] / nodeDict.get((posPlayer, res), [1, 1])[0]
            reslist.append((value, move))
        # return the move with the maximum value of wins/visits
        return sorted(reslist, key = lambda x:x[0])[-1][1]

    return fxn

if __name__ == '__main__':
    b = Kalah(6)
    pos = Kalah.Position(b, [6, 4, 2, 0, 0, 2, 9, 0, 0, 2, 2, 6, 6, 9], 0)
    print(mcts_strategy(1000)(pos))

    pos = Kalah.Position(b, [0, 0, 2, 2, 6, 6, 9, 6, 4, 2, 0, 0, 2, 9], 1)
    print(mcts_strategy(1000)(pos))
