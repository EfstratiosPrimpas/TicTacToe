import tkinter as tk
import random
from tkinter import messagebox


class TicTacToe(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.player1 = "X"
        self.player2 = "O"
        self.current_player = self.player1
        self.board = [" "]*9
        self.winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.game_mode = tk.StringVar(value="Player vs Player")
        self.board_frame = tk.Frame(self.master)
        self.buttons = []
        self.status_bar = tk.Label(self.master, text="Player {}'s turn".format(self.current_player), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.mode_frame = tk.Frame(self.master)
        self.player_vs_player_radio = tk.Radiobutton(self.mode_frame, text="Player vs Player", variable=self.game_mode, value="Player vs Player", command=self.reset_game)
        self.player_vs_computer_radio = tk.Radiobutton(self.mode_frame, text="Player vs Computer", variable=self.game_mode, value="Player vs Computer", command=self.reset_game)
        self.computer_vs_computer_radio = tk.Radiobutton(self.mode_frame, text="Computer vs Computer", variable=self.game_mode, value="Computer vs Computer", command=self.reset_game)
        self.reset_button = tk.Button(self.mode_frame, text="Reset Game", command=self.reset_game)
        self.setup_widgets()
        self.top_scores = {"Easy": [], "Medium": [], "Hard": []}

    def create_radio_button(self, text, value):
        return tk.Radiobutton(self.mode_frame, text=text, variable=self.game_mode, value=value, command=self.reset_game)

    def setup_widgets(self):
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(padx=10, pady=10)

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.board_frame, text="", width=5, height=2, font=("Helvetica", 20),
                               command=lambda idx=i: self.play(idx))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        self.status_bar = tk.Label(self.master, text="Player {}'s turn".format(self.current_player), bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.mode_frame = tk.Frame(self.master)
        self.mode_frame.pack(padx=10, pady=5)
        self.player_vs_player_radio = tk.Radiobutton(self.mode_frame, text="Player vs Player", variable=self.game_mode, value="Player vs Player", command=self.reset_game)
        self.player_vs_player_radio.pack(side=tk.LEFT)
        self.player_vs_computer_radio = tk.Radiobutton(self.mode_frame, text="Player vs Computer", variable=self.game_mode, value="Player vs Computer", command=self.reset_game)
        self.player_vs_computer_radio.pack(side=tk.LEFT)
        self.computer_vs_computer_radio = tk.Radiobutton(self.mode_frame, text="Computer vs Computer", variable=self.game_mode, value="Computer vs Computer", command=self.reset_game)
        self.computer_vs_computer_radio.pack(side=tk.LEFT)
        self.difficulty_label = tk.Label(self.mode_frame, text="Difficulty:")
        self.difficulty_label.pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="Easy")
        self.difficulty_menu = tk.OptionMenu(self.mode_frame, self.difficulty_var, "Easy", "Medium", "Hard")
        self.difficulty_menu.pack(side=tk.LEFT)
        self.reset_button = tk.Button(self.mode_frame, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(side=tk.RIGHT)

    def reset_game(self):
        self.current_player = self.player1
        self.board = [" "]*9
        self.reset_board_colors()
        self.status_bar.config(text="Player {}'s turn".format(self.current_player))
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)
        if self.game_mode.get() == "Computer vs Computer":
            self.play_computer()

    def reset_board_colors(self):
        for button in self.buttons:
            button.config(bg="SystemButtonFace")

    def play(self, idx):
        if self.board[idx] == " ":
            self.board[idx] = self.current_player
            self.buttons[idx].config(text=self.current_player, state=tk.DISABLED)
            winner = self.check_win()
            if winner:
                self.end_game(winner)
            elif " " not in self.board:
                self.end_game()
            else:
                self.current_player = self.player2 if self.current_player == self.player1 else self.player1
                self.status_bar.config(text="Player {}'s turn".format(self.current_player))
                if self.game_mode.get() == "Player vs Computer" and self.current_player == self.player2:
                    self.play_computer()

    def play_computer(self):
        if self.game_mode.get() == "Player vs Computer":
            player = self.player2
            print("Difficulty level: ", self.difficulty_var.get())
        else:
            player = self.current_player
        # Δημιουργία λίστας με τα κενά κελιά του πίνακα. Για κάθε αριθμό i στο εύρος 0-8,
        # ελέγχει αν το κελί με δείκτη i στον πίνακα self.board είναι κενό
        empty_cells = [i for i in range(9) if self.board[i] == " "]
        if empty_cells:
            if player == self.player1:
                idx = self.get_best_move(self.board, player)
            else:
                if self.difficulty_var.get() == "Easy":
                    idx = random.choice(empty_cells)
                elif self.difficulty_var.get() == "Medium":
                    # H random παράγει είτε 0 είτε 1 και έαν ο παραγόμενος αριθμός είναι 0,
                    # τότε ο υπολογιστής επιλέγει την get_best_move
                    if random.random() < 0.5:
                        idx = self.get_best_move(self.board, player)
                    else:
                        idx = random.choice(empty_cells)
                else:  # self.difficulty_var == "Hard"
                    idx = self.get_best_move(self.board, player)
            self.play(idx)
            #player = self.player1 if player == self.player2 else self.player2

    def get_best_move(self, board, player):
        best_score = -1000
        best_move = None
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score = self.minimax(board, False)
                board[i] = " "
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, is_maximizing):
        winner = self.check_win(board)
        if winner:
            if winner == self.player1:
                return -1
            else:
                return 1
        elif " " not in board:
            return 0
        else:
            if is_maximizing:
                best_score = -1000
                for i in range(9):
                    if board[i] == " ":
                        board[i] = self.player2
                        score = self.minimax(board, False)
                        board[i] = " "
                        best_score = max(score, best_score)
                return best_score
            else:
                best_score = 1000
                for i in range(9):
                    if board[i] == " ":
                        board[i] = self.player1
                        score = self.minimax(board, True)
                        board[i] = " "
                        best_score = min(score, best_score)
                return best_score

    def check_win(self, board=None):
        if not board:
            board = self.board
        for combination in self.winning_combinations:
            if board[combination[0]] == board[combination[1]] == board[combination[2]] != " ":
                return board[combination[0]]
        return None

    def end_game(self, winner=None):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        if winner:
            for combination in self.winning_combinations:
                if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != " ":
                    for idx in combination:
                        self.buttons[idx].config(bg="light green")
                    break
            messagebox.showinfo("Game Over", "Player {} wins!".format(winner))
        else:
            messagebox.showinfo("Game Over", "It's a tie!")


root = tk.Tk()
root.title('Tic-Tac-Toe Game')
game = TicTacToe(root)
root.mainloop()
