# I will now prepare the corrected Pygame code for the user with the 5 specified fixes.

import pygame
move_log = []
import sys
import os
import cairosvg
import io

WIDTH, HEIGHT = 1024, 768
FPS = 60
ASSETS_PATH = r"C:/Users/Ayan/Documents/ai/project/Assets/p1/"
BOARD_IMAGE_PATH = r"C:/Users/Ayan/Documents/ai/project/Assets/boards/rect-8x8.svg"
PIECE_SIZE = (64, 64)
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Chess - Student Project")
clock = pygame.time.Clock()

font = pygame.font.SysFont("DejaVu Sans", 32)
title_font = pygame.font.SysFont("DejaVu Sans", 42, bold=True)
small_font = pygame.font.SysFont("DejaVu Sans", 20)
split_font = pygame.font.SysFont("DejaVu Sans", 18, bold=True)

def load_svg_image(svg_path, size):
    png_bytes = cairosvg.svg2png(url=svg_path, output_width=size[0], output_height=size[1])
    return pygame.image.load(io.BytesIO(png_bytes)).convert_alpha()

background_img = pygame.image.load(os.path.join(ASSETS_PATH, "Bishop1.png"))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
board_image = load_svg_image(BOARD_IMAGE_PATH, (BOARD_SIZE, BOARD_SIZE))

piece_name_map = {"K": "king", "Q": "queen", "R": "rook", "B": "bishop", "N": "knight", "P": "pawn"}
pieces_images = {}
for color in ("w", "b"):
    for piece in ("K", "Q", "R", "B", "N", "P"):
        name = piece_name_map[piece]
        path = os.path.join(ASSETS_PATH, f"{name}-{color}.svg")
        pieces_images[f"{color}{piece}"] = load_svg_image(path, PIECE_SIZE)

def animated_text(surface, lines, font, color, x, y, delay=50):
    current_y = y
    rendered_lines = [""] * len(lines)
    for line_idx, line in enumerate(lines):
        for char in line:
            rendered_lines[line_idx] += char
            surface.blit(background_img, (0, 0))
            pygame.draw.rect(surface, (40, 40, 40), surface.get_rect(), 15)
            pygame.draw.rect(surface, (80, 80, 80), surface.get_rect(), 5)
            temp_y = y
            for text in rendered_lines:
                text_surface = font.render(text, True, color)
                surface.blit(text_surface, (x, temp_y))
                temp_y += font.get_height() + 10
            pygame.display.update()
            pygame.time.wait(delay)

def welcome_screen():
    animated_text(screen, ["Welcome to Quantum Chess", "Do you have the skills to play this?"], font, (255, 255, 255), 120, 300)
    while True:
        screen.blit(background_img, (0, 0))
        msg = small_font.render("Press any key to start...", True, (255, 255, 255))
        screen.blit(msg, ((WIDTH - msg.get_width()) // 2, 600))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                return

def side_selection():
    while True:
        screen.blit(background_img, (0, 0))
        pygame.draw.rect(screen, (40, 40, 40), screen.get_rect(), 15)
        pygame.draw.rect(screen, (80, 80, 80), screen.get_rect(), 5)
        title = title_font.render("NOW PLAYER, WHAT WOULD YOU LIKE TO BE", True, (255, 255, 255))
        option1 = font.render("A WHITE HEROIC KNIGHT", True, (200, 200, 200))
        option2 = font.render("OR A DARK NIGHT", True, (200, 200, 200))
        instruction = small_font.render("Press W for White | Press B for Black", True, (180, 180, 180))
        screen.blit(title, ((WIDTH - title.get_width()) // 2, 200))
        screen.blit(option1, ((WIDTH - option1.get_width()) // 2, 300))
        screen.blit(option2, ((WIDTH - option2.get_width()) // 2, 360))
        screen.blit(instruction, ((WIDTH - instruction.get_width()) // 2, 500))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: return 'w'
                elif event.key == pygame.K_b: return 'b'

def init_board():
    board = [[None for _ in range(8)] for _ in range(8)]
    order = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    for i in range(8):
        board[0][i] = ('b' + order[i], 1.0)
        board[1][i] = ('bP', 1.0)
        board[6][i] = ('wP', 1.0)
        board[7][i] = ('w' + order[i], 1.0)
    return board

def get_valid_moves(board, r, c):
    piece, _ = board[r][c]
    color, p_type = piece[0], piece[1]
    moves = []
    if p_type == 'P':
        dir = -1 if color == 'w' else 1
        start_row = 6 if color == 'w' else 1
        # Single move
        if 0 <= r + dir < 8 and not board[r + dir][c]:
            moves.append((r + dir, c))
            # Double move from start position
            if r == start_row and not board[r + 2 * dir][c]:
                moves.append((r + 2 * dir, c))
        # Captures
        for dc in [-1, 1]:
            nr, nc = r + dir, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and board[nr][nc] and board[nr][nc][0][0] != color:
                moves.append((nr, nc))
    elif p_type == 'N':
        for dr, dc in [(2, 1), (2, -1), (-2, 1), (-2, -1),
                       (1, 2), (1, -2), (-1, 2), (-1, -2)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 8 and 0 <= nc < 8 and (not board[nr][nc] or board[nr][nc][0][0] != color):
                moves.append((nr, nc))
    elif p_type in 'BRQ':
        directions = []
        if p_type in 'BQ':
            directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        if p_type in 'RQ':
            directions += [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while 0 <= nr < 8 and 0 <= nc < 8:
                if not board[nr][nc]:
                    moves.append((nr, nc))
                elif board[nr][nc][0][0] != color:
                    moves.append((nr, nc))
                    break
                else:
                    break
                nr += dr
                nc += dc
    elif p_type == 'K':
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < 8 and 0 <= nc < 8 and (not board[nr][nc] or board[nr][nc][0][0] != color):
                    moves.append((nr, nc))
    return moves

import random

class QuantumPiece:
    def __init__(self, pos, piece):
        self.piece = piece          # e.g. 'wP'
        self.qnum = {'0': [pos, 1]} # states: key=state_id, value=[pos, probability]
        self.ent = []

    def measure(self):
        total_prob = sum([self.qnum[state][1] for state in self.qnum])
        rnd = random.uniform(0, total_prob)
        cumulative = 0
        chosen_state = None
        for state in self.qnum:
            cumulative += self.qnum[state][1]
            if rnd <= cumulative:
                chosen_state = state
                break

        final_pos = self.qnum[chosen_state][0]
        self.qnum.clear()
        self.ent.clear()
        self.qnum['0'] = [final_pos, 1]               # entanglement relationships

Qpieces = []  # global list of QuantumPiece objects

def create_quantum_board(board):
    """Called after init_board() to populate Qpieces list."""
    Qpieces.clear()
    for r in range(8):
        for c in range(8):
            if board[r][c]:
                q_piece = QuantumPiece((r, c), board[r][c][0])  # only store piece type
                Qpieces.append(q_piece)

def find_quantum_piece(square):
    """Return (q_piece, state) if square matches any quantum state."""
    for qp in Qpieces:
        for state in qp.qnum:
            if qp.qnum[state][0] == square:
                return qp, state
    return None, None


def get_between_squares(start, end):
    """Return list of squares strictly between start and end (row,col)."""
    sr, sc = start
    er, ec = end
    squares = []

    dr = er - sr
    dc = ec - sc

    # Only straight lines or diagonals
    if dr != 0:
        dr_step = dr // abs(dr)
    else:
        dr_step = 0
    if dc != 0:
        dc_step = dc // abs(dc)
    else:
        dc_step = 0

    if dr_step == 0 and dc_step == 0:
        return []

    r, c = sr + dr_step, sc + dc_step
    while (r, c) != (er, ec):
        squares.append((r, c))
        r += dr_step
        c += dc_step
    return squares

def entangle_oneblock(self, my_state, target_pos, other_piece, other_state):
    """Add entanglement between self and other_piece."""
    x = self.qnum[my_state][1]
    y = other_piece.qnum[other_state][1]

    a = x * y
    b = x * (1 - y)

    self.qnum[my_state + '0'] = [self.qnum[my_state][0], a]
    self.qnum[my_state + '1'] = [target_pos, b]
    del self.qnum[my_state]

    last_state = other_state[:-1] + str(int(not int(other_state[-1])))

    other_piece.ent += [(self, my_state + '1', other_state), (self, my_state + '0', last_state)]
    self.ent += [(other_piece, other_state, my_state + '1'), (other_piece, last_state, my_state + '0')]

# Attach to QuantumPiece
setattr(QuantumPiece, "entangle_oneblock", entangle_oneblock)

def draw_board(board, selected=None, valid_moves=[], quantum_mode=False, player_color='w', computer_thinking=False, move_log=None):
    screen.blit(background_img, (0, 0))
    screen.blit(board_image, ((WIDTH - BOARD_SIZE) // 2, (HEIGHT - BOARD_SIZE) // 2))
    if computer_thinking:
        thinking_text = small_font.render("Computer thinking...", True, (255, 255, 0))
        screen.blit(thinking_text, (WIDTH - 250, HEIGHT - 30))
    x_offset, y_offset = (WIDTH - BOARD_SIZE) // 2, (HEIGHT - BOARD_SIZE) // 2
    for r in range(8):
        for c in range(8):
            board_r = 7 - r if player_color == 'b' else r
            board_c = 7 - c if player_color == 'b' else c
            if (board_r, board_c) in valid_moves:
                color = (255, 255, 0) if quantum_mode else (144, 238, 144)
                pygame.draw.rect(screen, color, (x_offset + c * SQUARE_SIZE, y_offset + r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    if selected:
        row, col = selected
        s_r = 7 - row if player_color == 'b' else row
        s_c = 7 - col if player_color == 'b' else col
        pygame.draw.rect(screen, (255, 0, 0), (x_offset + s_c * SQUARE_SIZE, y_offset + s_r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
    for r in range(8):
        for c in range(8):
            board_r = 7 - r if player_color == 'b' else r
            board_c = 7 - c if player_color == 'b' else c
            piece = board[board_r][board_c]
            if piece:
                img = pieces_images[piece[0]]
                q_piece, q_state = find_quantum_piece((board_r, board_c))
                if q_piece and q_piece.ent:
                    pygame.draw.circle(screen, (255, 255, 0),
                                       (x_offset + c * SQUARE_SIZE + SQUARE_SIZE // 2,
                                        y_offset + r * SQUARE_SIZE + SQUARE_SIZE // 2),
                                       10)
                screen.blit(img, (x_offset + c * SQUARE_SIZE, y_offset + r * SQUARE_SIZE))
                if piece[1] == 0.5:
                    overlay = split_font.render("50%", True, (255, 0, 0))
                    screen.blit(overlay, (x_offset + c * SQUARE_SIZE + 5, y_offset + r * SQUARE_SIZE + 5))
    mode_msg = small_font.render(f"Quantum Mode: {'ON' if quantum_mode else 'OFF'} (Toggle Q)", True, (255, 255, 255))
    screen.blit(mode_msg, (10, HEIGHT - 30))

    # Draw move log panel
    if move_log:
        pygame.draw.rect(screen, (30, 30, 30), (WIDTH - 200, 50, 180, 140))
        log_title = small_font.render("Last 4 Moves", True, (255, 255, 255))
        screen.blit(log_title, (WIDTH - 190, 55))
        for i, move_text in enumerate(move_log[-4:]):
            move_surf = small_font.render(move_text, True, (200, 200, 200))
            screen.blit(move_surf, (WIDTH - 190, 80 + i * 25))

def is_in_check(board, color):
    king_pos = None
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0] == color + 'K':
                king_pos = (r, c)
                break
        if king_pos:
            break
    if not king_pos:
        return True  # No king = checkmate
    enemy_color = 'b' if color == 'w' else 'w'
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0][0] == enemy_color:
                moves = get_valid_moves(board, r, c)
                if king_pos in moves:
                    return True
    return False

def has_valid_moves(board, color):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece and piece[0][0] == color:
                moves = get_valid_moves(board, r, c)
                for move in moves:
                    new_board = [row.copy() for row in board]
                    new_board[move[0]][move[1]] = new_board[r][c]
                    new_board[r][c] = None
                    if not is_in_check(new_board, color):
                        return True
    return False

def computer_move(board, color):
    computer_quantum_chance = 0.25
    computer_collapse_chance = 0.15
    pieces = [(r, c) for r in range(8) for c in range(8)
              if board[r][c] and board[r][c][0][0] == color]
    random.shuffle(pieces)

    # 🟢 New: try collapse first
    for r, c in pieces:
        q_piece, q_state = find_quantum_piece((r, c))
        if q_piece and len(q_piece.qnum) > 1 and random.random() < computer_collapse_chance:
            q_piece.measure()
            return

    # 🔵 normal move or split
    for r, c in pieces:
        moves = get_valid_moves(board, r, c)
        if moves:
            if random.random() < computer_quantum_chance and not any(board[r][c][1] == 0.5 for _ in [1]):
                empty_squares = [(rr, cc) for rr in range(8) for cc in range(8)
                                 if not board[rr][cc] and (rr, cc) != (r, c)]
                if len(empty_squares) >= 2:
                    split1, split2 = random.sample(empty_squares, 2)
                    piece = board[r][c][0]
                    board[split1[0]][split1[1]] = (piece, 0.5)
                    board[split2[0]][split2[1]] = (piece, 0.5)
                    board[r][c] = None
                    return
            move = random.choice(moves)
            board[move[0]][move[1]] = board[r][c]
            board[r][c] = None
            move_log.append(f"C: {chr(c+97)}{8-r}→{chr(move[1]+97)}{8-move[0]}")
            return
    pieces = [(r, c) for r in range(8) for c in range(8)
              if board[r][c] and board[r][c][0][0] == color]
    random.shuffle(pieces)
    for r, c in pieces:
        moves = get_valid_moves(board, r, c)
        if moves:
            move = random.choice(moves)
            board[move[0]][move[1]] = board[r][c]
            board[r][c] = None
            break

def check_game_over(board, player_color):
    if is_in_check(board, player_color):
        if not has_valid_moves(board, player_color):
            return True, 'black' if player_color == 'w' else 'white'
    else:
        if not has_valid_moves(board, player_color):
            return True, 'draw'
    return False, None



def main():
    global move_log
    welcome_screen()
    player_color = side_selection()
    computer_color = 'b' if player_color == 'w' else 'w'
    board = init_board()
    create_quantum_board(board)  # NEW: populate Qpieces
    selected, valid_moves, run = None, [], True
    quantum_mode = False
    game_over = False
    winner = None

    while run:
        draw_board(board, selected, valid_moves, quantum_mode, player_color, computer_thinking=False, move_log=move_log)
        if game_over:
            end_msg = f"Game Over! {'Draw' if winner == 'draw' else winner.capitalize() + ' Wins!'}"
            text_surface = font.render(end_msg, True, (255, 255, 255))
            screen.blit(text_surface, ((WIDTH - text_surface.get_width()) // 2, 20))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            continue

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m and selected:
                    q_piece, q_state = find_quantum_piece(selected)
                    if q_piece:
                        q_piece.measure()
                if event.key == pygame.K_q:
                    quantum_mode = not quantum_mode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                x_off, y_off = (WIDTH - BOARD_SIZE) // 2, (HEIGHT - BOARD_SIZE) // 2
                col, row = (mx - x_off) // SQUARE_SIZE, (my - y_off) // SQUARE_SIZE
                board_row = 7 - row if player_color == 'b' else row
                board_col = 7 - col if player_color == 'b' else col
                if 0 <= board_row < 8 and 0 <= board_col < 8:
                    if selected:
                        sr, sc = selected
                        piece = board[sr][sc]
                        target = board[board_row][board_col]
                        if target and target[0][0] == piece[0][0]:
                            selected, valid_moves = None, []
                        elif (board_row, board_col) in valid_moves:
                            if quantum_mode and not target:
                                if piece[1] == 1.0:
                                    board[board_row][board_col] = (piece[0], 0.5)
                                    board[sr][sc] = (piece[0], 0.5)
                            else:
                                between = get_between_squares((sr, sc), (board_row, board_col))
                                q_found = []
                                for sq in between:
                                    q_piece, q_state = find_quantum_piece(sq)
                                    if q_piece:
                                        q_found.append((q_piece, q_state))
                                if len(q_found) == 1:
                                    my_q_piece, my_q_state = find_quantum_piece((sr, sc))
                                    if my_q_piece:
                                        my_q_piece.entangle_oneblock(my_q_state, (board_row, board_col),
                                                                     q_found[0][0], q_found[0][1])
                                        board[sr][sc] = None
                                else:
                                    board[board_row][board_col] = board[sr][sc]
                                    board[sr][sc] = None
                            move_log.append(f"P: {chr(sc+97)}{8-sr}→{chr(board_col+97)}{8-board_row}")
                            opponent_color = 'b' if player_color == 'w' else 'w'
                            game_over, winner = check_game_over(board, opponent_color)
                            if not game_over and opponent_color == computer_color:
                                computer_move(board, computer_color)
                                game_over, winner = check_game_over(board, player_color)
                        selected, valid_moves = None, []
                    elif board[board_row][board_col] and board[board_row][board_col][0][0] == player_color:
                        selected = (board_row, board_col)
                        valid_moves = get_valid_moves(board, board_row, board_col)
        clock.tick(FPS)

if __name__ == "__main__":
    main()
