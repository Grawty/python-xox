import pygame
import sys
import math
import random

pygame.init()

WINDOW_WIDTH = 350
WINDOW_HEIGHT = 350
BG_COLOR = (0, 0, 0)
LINE_COLOR = (255, 255, 255)
BOARD_SIZE = 3
SQUARE_SIZE = 90
BOARD_MARGIN = 40
FONT_SIZE = 40

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

font = pygame.font.SysFont(None, FONT_SIZE)

board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

human_player = 'X'
ai_player = 'O'

game_over = False
winner = None

EASY = 1
MEDIUM = 2
HARD = 3

def draw_board():
    win.fill(BG_COLOR)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            pygame.draw.rect(win, LINE_COLOR, (BOARD_MARGIN + j * SQUARE_SIZE, BOARD_MARGIN + i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
            if board[i][j] != ' ':
                text = font.render(board[i][j], True, LINE_COLOR)
                win.blit(text, (BOARD_MARGIN + j * SQUARE_SIZE + SQUARE_SIZE//2 - text.get_width()//2, BOARD_MARGIN + i * SQUARE_SIZE + SQUARE_SIZE//2 - text.get_height()//2))

def check_game_over():
    global game_over, winner
    
    for i in range(BOARD_SIZE):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != ' ':
            game_over = True
            winner = board[i][0]
            return
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != ' ':
            game_over = True
            winner = board[0][i]
            return
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
            game_over = True
            winner = board[0][0]
            return
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        game_over = True
        winner = board[0][2]
        return
    
    if all([board[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)]):
        game_over = True
        return

def player_move(row, col):
    if board[row][col] == ' ':
        board[row][col] = human_player

def minimax(board_state, depth, player):
    if player == ai_player:
        best_score = -math.inf
    else:
        best_score = math.inf

    if check_win(board_state, human_player):
        return -1
    elif check_win(board_state, ai_player):
        return 1
    elif check_tie(board_state):
        return 0

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board_state[i][j] == ' ':
                board_state[i][j] = player
                score = minimax(board_state, depth + 1, human_player if player == ai_player else ai_player)
                board_state[i][j] = ' '
                if player == ai_player:
                    best_score = max(score, best_score)
                else:
                    best_score = min(score, best_score)

    return best_score

def check_tie(board_state):
    return all([board_state[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)])

def check_win(board_state, player):
    for i in range(BOARD_SIZE):
        if all([board_state[i][j] == player for j in range(BOARD_SIZE)]):
            return True

        if all([board_state[j][i] == player for j in range(BOARD_SIZE)]):
            return True

    if all([board_state[i][i] == player for i in range(BOARD_SIZE)]):
        return True

    if all([board_state[i][BOARD_SIZE - i - 1] == player for i in range(BOARD_SIZE)]):
        return True

    return False

def ai_move():
    best_score = -math.inf
    best_move = None

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == ' ':
                board[i][j] = ai_player
                score = minimax(board, 0, human_player)
                board[i][j] = ' '

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    if best_move is not None:
        row, col = best_move
        board[row][col] = ai_player

    check_game_over()

    if winner:
        pygame.display.set_caption(f"{winner} wins!")
    elif game_over:
        pygame.display.set_caption("DRAW!")
    else:
        pygame.display.set_caption("Tic Tac Toe")

def reset_game():
    global board, game_over, winner
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    game_over = False
    winner = None
    pygame.display.set_caption("Tic Tac Toe")

def game_loop():
    player_turn = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and player_turn and not game_over:
                if pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    row = (y - BOARD_MARGIN) // SQUARE_SIZE
                    col = (x - BOARD_MARGIN) // SQUARE_SIZE
                    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                        if board[row][col] == ' ':
                            player_move(row, col)
                            player_turn = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        if not game_over and winner is None and not player_turn:
            ai_move()
            player_turn = True

        check_game_over()
        draw_board()
        pygame.display.update()

game_loop()

# GRWTY
