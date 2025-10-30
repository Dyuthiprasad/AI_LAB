import math

def print_board(board):
    for row in board:
        print(row)
    print()

def is_moves_left(board):
    for row in board:
        if "_" in row:
            return True
    return False

def evaluate(board):
    for row in board:
        if row.count('X') == 3:
            return 10
        elif row.count('O') == 3:
            return -10
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            if board[0][col] == 'X':
                return 10
            elif board[0][col] == 'O':
                return -10
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == 'X':
            return 10
        elif board[0][0] == 'O':
            return -10
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == 'X':
            return 10
        elif board[0][2] == 'O':
            return -10
    return 0


def alpha_beta(board, depth, alpha, beta, isMax):
    score = evaluate(board)

    if score == 10 or score == -10:
        return score
    if not is_moves_left(board):
        return 0

    if isMax:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = 'X'
                    val = alpha_beta(board, depth + 1, alpha, beta, False)
                    board[i][j] = "_"
                    best = max(best, val)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == "_":
                    board[i][j] = 'O'
                    val = alpha_beta(board, depth + 1, alpha, beta, True)
                    board[i][j] = "_"
                    best = min(best, val)
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best


def find_best_move_alpha_beta(board):
    best_val = -math.inf
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == "_":
                board[i][j] = 'X'
                move_val = alpha_beta(board, 0, -math.inf, math.inf, False)
                board[i][j] = "_"
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    print("Best move value:", best_val)
    return best_move


# Example board
board = [
    ['X', 'O', 'X'],
    ['O', 'O', '_'],
    ['_', '_', 'X']
]

print_board(board)
best = find_best_move_alpha_beta(board)
print("Best move for X is:", best)
