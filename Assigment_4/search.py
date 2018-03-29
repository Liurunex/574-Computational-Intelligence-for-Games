from kalah import Kalah

def depth_limited_search_strategy(depth, h):
    def fxn(pos):
        value, move = search_limited(pos, depth, h)
        return move
    return fxn

def depth_unlimited_search_strategy(depth, h):
    def fxn(pos):
        low, up, move = search_unlimited(pos, depth, h)
        return move
    return fxn

def search_limited(pos, depth, h):
    return alpha_beta(pos, depth, h, -h.inf, h.inf)

ttable = {}
def search_unlimited(pos, depth, h):
    return alpha_beta_TTable(pos, depth, h, -h.inf, h.inf, ttable)

def alpha_beta(pos, depth, h, alpha, beta):
    if pos.game_over() or depth == 0:
        return (h.evaluate(pos), None)
    else:
        if pos.next_player() == 0:
            # max player
            best_value = -h.inf
            best_move = None
            moves = pos.legal_moves()
            for move in moves:
                child = pos.result(move)
                mm, _ = alpha_beta(child, depth - 1, h, alpha, beta)
                if mm > best_value:
                    best_value = mm
                    best_move = move
                alpha = max(alpha, best_value)
                # Alpha Beta Pruning
                if alpha >= beta:
                    break
            return (best_value, best_move)
        else:
            # min player
            best_value = h.inf
            best_move = None
            moves = pos.legal_moves()
            for move in moves:
                child = pos.result(move)
                mm, _ = alpha_beta(child, depth - 1, h, alpha, beta)
                if mm < best_value:
                    best_value = mm
                    best_move = move
                beta = min(beta, best_value)
                 # Alpha Beta Pruning
                if alpha >= beta:
                    break
            return (best_value, best_move)

def alpha_beta_TTable(pos, depth, h, alpha, beta, ttable):
    # transpotation table
    if pos in ttable:
        low, up, d, mv = ttable[pos]
        if d >= depth:
            if low == up:
                return (low, up, mv)
            if (low >= beta):
                return (low, up, mv)
            if (up <= alpha):
                return (low, up, mv)

    if pos.game_over():
        value = h.evaluate(pos)
        return (value, value, None)

    if depth == 0:
        value = h.evaluate(pos)
        ttable[pos] = (value, value, depth, None)
        return (value, value, None)

    else:
        if pos.next_player() == 0:
            # max player
            bound = (-h.inf, -h.inf)
            best_move = None
            moves = pos.legal_moves()
            count = 0
            
            for move in moves:
                count += 1
                child = pos.result(move)
                nb0, nb1, nmove = alpha_beta_TTable(child, depth - 1, h, alpha, beta, ttable)
                if bound[0] < nb0 or bound[1] < nb1:
                    best_move = move
                bound = (max(bound[0], nb0), max(bound[1], nb1))
                alpha = max(alpha, bound[0])
                # Alpha Beta Pruning
                if alpha >= beta:
                    break
            if count != len(moves):
                bound = (bound[0], h.inf)
            ttable[pos] = (bound[0], bound[1], depth, best_move)
            return (bound[0], bound[1], best_move)
        else:
            # min player
            bound = (h.inf, h.inf)
            best_move = None
            moves = pos.legal_moves()
            count = 0

            for move in moves:
                count += 1
                child = pos.result(move)
                nb0, nb1, nmove = alpha_beta_TTable(child, depth - 1, h, alpha, beta, ttable)
                if bound[0] > nb0 or bound[1] > nb1:
                    best_move = move
                bound = (min(bound[0], nb0), min(bound[1], nb1))
                beta = min(beta, bound[1])
                 # Alpha Beta Pruning
                if alpha >= beta:
                    break
            if count != len(moves):
                bound = (-h.inf, bound[1])
            ttable[pos] = (bound[0], bound[1], depth, best_move)
            return (bound[0], bound[1], best_move)