import random
import datetime
from math import log, sqrt

# wins and plays are the record table used to store the game tree
wins = {}
plays = {}
#seconds = 0.1
#calculation_time = datetime.timedelta(seconds=seconds)
max_moves = 100
max_sims = 100
C = 1
r = random.Random(500)

def mcts_strategy(n):
    def fxn(p):
        move = mcts(p)
        return move
    return fxn

def run_simulation(pos):
    # A bit of an optimization here, so we have a local
    # variable lookup instead of an attribute access each loop.

    visited_pos = set()
    player = pos.next_player()
    expand = True
    cur_pos = pos

    for t in range(1, max_moves + 1):
        legal = cur_pos.legal_moves()
        move_pos = [(move_, cur_pos.result(move_)) for move_ in legal]

        if all(plays.get((player, pos_)) for move_, pos_ in move_pos):
            # If we have stats on all of the legal moves here, use them.
            log_total = 2 * log(sum(plays[(player, pos_)] for move_, pos_ in move_pos))
            value, best_move, best_pos = max(
                ((wins[(player, pos_)] / plays[(player, pos_)]) +
                 C * sqrt(log_total / plays[(player, pos_)]), move_, pos_)
                for move_, pos_ in move_pos
            )
        else:
            # Otherwise, just make an random decision.
            best_move, best_pos = r.choice(move_pos)

        cur_pos = best_pos

        # `player` here and below refers to the player
        # who moved into that particular state.
        if expand and (player, cur_pos) not in plays:
            expand = False
            plays[(player, cur_pos)] = 0
            wins[(player, cur_pos)] = 0

        visited_pos.add((player, cur_pos))
        #reset the player
        player = cur_pos.next_player()
        if cur_pos.game_over():
            winner = cur_pos.winner()
            break
    # back propagation
    for player_, pos_ in visited_pos:
        if (player_, pos_) not in plays:
            continue
        plays[(player_, pos_)] += 1
        if (player_ == 0 and winner == 1) or (player_ == 1 and winner == -1):
            wins[(player_, pos_)] += 1

def mcts(pos):
    # clear out the tree at the start of each game
    if pos.is_initial():
        wins.clear()
        plays.clear()

    legal = pos.legal_moves()
    # if there's no legal move or a single legal move, return
    if not legal:
        return
    if len(legal) == 1:
        return legal[0]
    # for a limited reps, run simulation on the game tree
    sims = 0
    begin = datetime.datetime.utcnow()
    while sims < max_sims:#datetime.datetime.utcnow() - begin < calculation_time:
        run_simulation(pos)
        sims += 1
    # the entries of the record table
    move_pos = [(move_, pos.result(move_)) for move_ in legal]
    #print("wins size:", len(wins), " plays size:", len(plays))
    # Pick the move with the highest percentage of wins.
    player = pos.next_player()
    percent_wins, best_move = max(
        (wins.get((player, pos_), 0) /
         plays.get((player, pos_), 1),
         move_)
        for move_, pos_ in move_pos
    )
    return best_move
