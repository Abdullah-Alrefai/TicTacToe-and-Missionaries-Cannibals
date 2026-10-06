# Tic-tac-toe agent using alpha-beta search.
#
# The board is a list of 9 cells indexed like this:
#   0 | 1 | 2
#   3 | 4 | 5
#   6 | 7 | 8
# Each cell is 'X', 'O', or ' ' (empty).

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def other(player):
    return 'O' if player == 'X' else 'X'


def winner(board):
    """Return 'X' or 'O' if that player has three in a row, otherwise None."""
    for a, b, c in LINES:
        if board[a] != ' ' and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_terminal(board):
    """A board is terminal if someone has won or there are no empty cells (draw)."""
    return winner(board) is not None or ' ' not in board


def utility(board, player):
    """Utility of a terminal board for player: +1 win, -1 loss, 0 draw."""
    w = winner(board)
    if w == player:
        return 1
    if w == other(player):
        return -1
    return 0


def legal_moves(board):
    return [i for i in range(9) if board[i] == ' ']


def alphabeta(board, to_move, player, alpha, beta):
    """Value of board from player's point of view, with to_move about to play."""
    if is_terminal(board):
        return utility(board, player)

    if to_move == player:
        value = float('-inf')
        for move in legal_moves(board):
            board[move] = to_move
            value = max(value, alphabeta(board, other(to_move), player, alpha, beta))
            board[move] = ' '
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in legal_moves(board):
            board[move] = to_move
            value = min(value, alphabeta(board, other(to_move), player, alpha, beta))
            board[move] = ' '
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


def choose_move(board, player):
    """Return the best legal move for player, or None if the board is terminal."""
    if is_terminal(board):
        return None

    best_move = None
    best_value = float('-inf')
    for move in legal_moves(board):
        board[move] = player
        value = alphabeta(board, other(player), player, float('-inf'), float('inf'))
        board[move] = ' '
        if value > best_value:
            best_value = value
            best_move = move
    return best_move


def play_game(agent_x, agent_o):
    """Play one game between two agents. Returns 'X', 'O', or 'Draw'."""
    board = [' '] * 9
    agents = {'X': agent_x, 'O': agent_o}
    to_move = 'X'
    while not is_terminal(board):
        move = agents[to_move](board, to_move)
        board[move] = to_move
        to_move = other(to_move)
    w = winner(board)
    return w if w is not None else 'Draw'


def run_self_play(n=20):
    """Two copies of the agent play n games, alternating which one plays X and O."""
    agent_a = choose_move
    agent_b = choose_move
    results = {'X': 0, 'O': 0, 'Draw': 0}
    for game in range(n):
        if game % 2 == 0:
            result = play_game(agent_a, agent_b)  # Agent A is X, Agent B is O
        else:
            result = play_game(agent_b, agent_a)  # Agent B is X, Agent A is O
        results[result] += 1
    print(f"Games played: {n}")
    print(f"X wins: {results['X']}")
    print(f"O wins: {results['O']}")
    print(f"Draws: {results['Draw']}")


# How the program was tested:
#
# The agent was given specific board positions and its chosen move (or the
# utility, for terminal boards) was compared with the expected behavior.
#
# Position 1 - immediate win (X to move):
#   X | X |
#   O | O |
#     |   |
#   Expected: choose_move returns 2, completing the top row and winning
#   immediately.
#
# Position 2 - block an opponent's immediate win (O to move):
#   X | X |
#     | O |
#     |   |
#   Expected: choose_move returns 2, blocking X from completing the top row.
#
# Position 3 - terminal board (X has already won):
#   X | X | X
#   O | O |
#     |   |
#   Expected: is_terminal is True, choose_move returns None (no move is
#   attempted), utility for X is +1 and utility for O is -1.
#
# The self-play run was also checked: since both agents play optimally,
# every game should end in a draw.

if __name__ == "__main__":
    run_self_play(20)
