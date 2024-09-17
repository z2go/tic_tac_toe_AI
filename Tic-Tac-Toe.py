from os import system
from xml.sax.saxutils import escape

import pygame
pygame.init()

from sympy import floor

screen_size = (720,720)
screen = pygame.display.set_mode(screen_size)
screen.fill((255, 255, 255))

#This function is used to draw the board's current state every time the user turn arrives. 
def draw_board(board):

    pygame.draw.line(screen,(0,0,0),(240,0),(240,720),3)
    pygame.draw.line(screen, (0, 0, 0), (480, 0), (480, 720), 3)

    pygame.draw.line(screen, (0, 0, 0), (0, 240), (720, 240), 3)
    pygame.draw.line(screen, (0, 0, 0), (0, 480), (720, 480), 3)
    for i in range (0,9):
        if (board[i]==1):
            pygame.draw.circle(screen,(0,0,0),(240*(i%3)+120, 240*(floor(i/3))+120),100,2)
        if(board[i]==-1):    
            pygame.draw.line(screen,(0,0,0), (240*(i%3)+20, 240*(floor(i/3))+20),(240*(i%3)+220, 240*(floor(i/3))+220))
            pygame.draw.line(screen, (0, 0, 0), (240 * (i % 3) + 20, 240 * (floor(i / 3)) + 220),(240 * (i % 3) + 220, 240 * (floor(i / 3)) + 20),2)
    pygame.display.flip()
#This function takes the user move as input and make the required changes on the board.


#MinMax function.
# Minimax function to evaluate all possible outcomes
def minimax(board, depth, is_maximizing):
    result = analyzeboard(board)

    # Base cases: return score based on the game outcome
    if result == 1:  # AI wins
        return 10 - depth  # Prefer faster wins
    elif result == -1:  # Human wins
        return depth - 10  # Prefer slower losses
    elif result == 0:  # Draw
        return 0

    if is_maximizing:  # AI's turn to maximize score
        best_score = -float('inf')
        for i in range(9):
            if board[i] == 0:  # Check for empty spot
                board[i] = 1  # AI is "O", represented by 1
                score = minimax(board, depth + 1, False)  # Recursively call minimax
                board[i] = 0  # Undo move
                best_score = max(score, best_score)  # Choose the maximum score
        return best_score
    else:  # Human's turn to minimize score
        best_score = float('inf')
        for i in range(9):
            if board[i] == 0:  # Check for empty spot
                board[i] = -1  # Human is "X", represented by -1
                score = minimax(board, depth + 1, True)  # Recursively call minimax
                board[i] = 0  # Undo move
                best_score = min(score, best_score)  # Choose the minimum score
        return best_score


#This function makes the computer's move using minmax algorithm.
def CompTurn(board):
    best_score = -float('inf')
    best_move = -1
    for i in range(9):
        if board[i] == 0:  # Check for empty spot
            board[i] = 1  # AI is "O", represented by 1
            score = minimax(board, 0, False)  # Call minimax for the move
            board[i] = 0  # Undo the move
            if score > best_score:  # Choose the move with the highest score
                best_score = score
                best_move = i

    board[best_move] = 1  # Make the best move for AI


#This function is used to analyze a game.
def analyzeboard(board):
    # All possible winning combinations
    winning_combinations = [
        [0, 1, 2],  # Top row
        [3, 4, 5],  # Middle row
        [6, 7, 8],  # Bottom row
        [0, 3, 6],  # Left column
        [1, 4, 7],  # Middle column
        [2, 5, 8],  # Right column
        [0, 4, 8],  # Left diagonal
        [2, 4, 6]  # Right diagonal
    ]

    # Check for a winner
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != 0:
            return board[combo[0]]  # Return 1 if "O" (AI) wins, -1 if "X" (human) wins

    # Check if the board is full (draw)
    if all(spot != 0 for spot in board):
        return 0  # Draw

    return -2

#Main Function.
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
def main():
    is_human_turn = True
    running = True

    while running:
        draw_board(board)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                column = floor(m_pos[0]/240)
                row = floor(m_pos[1]/240)

                if board[row*3+column] == 0:
                    board[row*3+column] = -1
                    is_human_turn = False
        x = analyzeboard(board)
        if (x == 0):
            print("Draw!!!")
            screen.fill((200,200,0))
            running = False
            break
        elif (x == -1):
            print("X Wins")
            screen.fill((0, 200, 0))
            running = False
            break
        else:
            draw_board(board)

        if not is_human_turn:
            CompTurn(board)
            is_human_turn = True


        x=analyzeboard(board)
        if(x==1):
            print("O Wins")
            screen.fill((200, 0, 0))
            running = False
        else:
            draw_board(board)

main()
while True:
    draw_board(board)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                screen.fill((255,255,255))
                board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
                main()

