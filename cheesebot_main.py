import chess
import random
import time


# determine sides
if random.random() < 0.5:
    white = True
    print("You are playing as Black")
else:
    white = False
    print("You are playing as White")

print("\n\n")
time.sleep(1.5)

# Sample openings dictionary
openings = {
    "e4 c5": "Sicilian Defense - 2.Nf3",
    "e4 e6": "French Defense - 2.d4",
    "e4 e5 Nf3 Nc6 Bb5": "Ruy Lopez - 4.a6",
}



def evaluate_board(board):
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }
    score = 0
    for piece in piece_values:
        score += len(board.pieces(piece, chess.WHITE)) * piece_values[piece]
        score -= len(board.pieces(piece, chess.BLACK)) * piece_values[piece]
    return score

def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval

def find_best_move(board, depth):
    best_move = None
    best_value = float('-inf')
    alpha = float('-inf')
    beta = float('inf')

    for move in board.legal_moves:
        board.push(move)
        move_value = alpha_beta(board, depth - 1, alpha, beta, False)
        board.pop()

        if move_value > best_value:
            best_value = move_value
            best_move = move
            alpha = max(alpha, move_value)

    return best_move

def check_opening(board):
    moves = [board.san(move) for move in board.move_stack]
    move_sequence = " ".join(moves)

    for opening in openings:
        if move_sequence.startswith(opening):
            return openings[opening]

    return None

def main():
    board = chess.Board()
    depth = 3  # Set the depth for the Minimax algorithm

    while not board.is_game_over():
        print(board)

        if white:
            if board.turn == chess.WHITE:
                move = find_best_move(board, depth)
                board.push(move)
                print(f"Bot plays: {move}")
            else:
                user_move = input("Your move (e2e4): ")
                board.push(chess.Move.from_uci(user_move))
        else:
            if board.turn == chess.WHITE:
                user_move = input("Your move (e2e4): ")
                board.push(chess.Move.from_uci(user_move))
            else:
                move = find_best_move(board, depth)
                board.push(move)
                print(f"Bot plays: {move}")
        # Check for openings after each move
        '''
        opening_response = check_opening(board)
        if opening_response:
            print(f"Bot recognized opening: {opening_response}")
        '''

        time.sleep(0.5)
        print("\n")

    print("Game over")

if __name__ == "__main__":
    main()
