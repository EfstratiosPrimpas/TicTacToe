import time
import pygame
import sys



#hello change here
# Initialize Pygame
pygame.init()

# Define the window size
window_size = (500, 500)

# Define the colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Create the game window
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tic Tac Toe")

# Define the font
font = pygame.font.SysFont(None, 50)

# Define the board
board = [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]

# Define the player
player = 1

# Define the game loop
while True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()

            # Get the row and column
            row = int(y // 166.666666667)
            col = int(x // 166.666666667)

            # Check if the cell is empty
            if board[row][col] == 0:

                # Update the board
                board[row][col] = player

                # Switch the player
                player = 3 - player

    # Clear the screen
    window.fill(white)

    # Draw the board
    pygame.draw.line(window, black, (166.666666667, 0), (166.666666667, 500), 2)
    pygame.draw.line(window, black, (333.333333333, 0), (333.333333333, 500), 2)
    pygame.draw.line(window, black, (0, 166.666666667), (500, 166.666666667), 2)
    pygame.draw.line(window, black, (0, 333.333333333), (500, 333.333333333), 2)

    # Draw the X's and O's
    for row in range(3):
        for col in range(3):
            if board[row][col] == 1:
                pygame.draw.line(window, red, (col * 166.666666667 + 20, row * 166.666666667 + 20), (col * 166.666666667 + 146, row * 166.666666667 + 146), 5)
                pygame.draw.line(window, red, (col * 166.666666667 + 146, row * 166.666666667 + 20), (col * 166.666666667 + 20, row * 166.666666667 + 146), 5)
            elif board[row][col] == 2:
                pygame.draw.circle(window, blue, (col * 166.666666667 + 83, row * 166.666666667 + 83), 70, 5)

    # Check for a winner
    winner = 0
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != 0:
            winner = board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != 0:
            winner = board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != 0:
            winner = board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != 0:
            winner = board[0][2]

        # Draw the winner
        if winner != 0:
            if winner == 1:

                text = font.render("Player 1 wins!", True, red)
        elif winner == 2:
            text = font.render("Player 2 wins!", True, blue)
        window.blit(text, (50, 225))

        # Check for a tie
        if winner == 0:
            tie = True
        for row in range(3):
            for col in range(3):

                if board[row][col] == 0:
                    tie = False
        if tie:
            text = font.render("Tie game!", True, black)
        window.blit(text, (150, 225))

        # Update the display
        pygame.display.update()
update
