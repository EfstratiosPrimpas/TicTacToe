import tkinter as tk
import random
from tkinter import messagebox


class TicTacToe(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.player1 = "X"
        self.player2 = "O"
        self.scores = {"X": 0, "O": 0}
        self.current_player = self.player1
        self.board = [" "]*9
        self.winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.game_mode = tk.StringVar(value="Player vs Player")
        self.board_frame = tk.Frame(self.master)
        self.game_number = 1
        self.buttons = []
        self.mode_frame = tk.Frame(self.master)
        self.player_vs_player_radio = tk.Radiobutton(self.mode_frame, text="Player vs Player", variable=self.game_mode,
                                                     value="Player vs Player", command=self.reset_game)
        self.player_vs_computer_radio = tk.Radiobutton(self.mode_frame, text="Player vs Computer", variable=self.game_mode,
                                                       value="Player vs Computer", command=self.reset_game)
        self.computer_vs_computer_radio = tk.Radiobutton(self.mode_frame, text="Computer vs Computer", variable=self.game_mode,
                                                         value="Computer vs Computer", command=self.reset_game)
        self.reset_button = tk.Button(self.mode_frame, text="Reset Game", command=self.reset_game)
        self.setup_widgets()

    def setup_widgets(self):
        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.score_label = tk.Label(self.master, text="Player X     {} : {}     Player O".format(self.scores["X"], self.scores["O"]))
        self.score_label.pack(side=tk.TOP, pady=10)
        self.master.update_idletasks()
        self.score_label.place(relx=0.5, y=0.5, anchor=tk.N)
        self.board_frame = tk.Frame(self.master, highlightbackground='#000000', bd=2)
        self.board_frame.pack(padx=10, pady=10)

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.board_frame, text="", width=5, height=2, font=("Helvetica", 40, "bold"),
                               command=lambda idx=i: self.play(idx))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        self.current_player_label = tk.Label(self.master, text="Player {}'s turn".format(self.current_player), bd=3,
                                             relief=tk.FLAT, anchor=tk.E, bg="#bdcdff", padx=20, pady=6,
                                             font=("Consolas", 12, "bold"), highlightthickness=2, highlightbackground="blue")
        self.current_player_label.place(relx=0.97, rely=0.2, anchor=tk.E)
        self.mode_frame = tk.Frame(self.master)
        self.mode_frame.pack(padx=200, pady=5)
        self.player_vs_player_radio = tk.Radiobutton(self.mode_frame, text="Player vs Player", variable=self.game_mode,
                                                     value="Player vs Player", command=self.reset_game)
        self.player_vs_player_radio.pack(side=tk.LEFT)
        self.player_vs_computer_radio = tk.Radiobutton(self.mode_frame, text="Player vs Computer",
                                                       variable=self.game_mode,
                                                       value="Player vs Computer", command=self.reset_game)
        self.player_vs_computer_radio.pack(side=tk.LEFT)
        self.computer_vs_computer_radio = tk.Radiobutton(self.mode_frame, text="Computer vs Computer",
                                                         variable=self.game_mode,
                                                         value="Computer vs Computer", command=self.reset_game)
        self.computer_vs_computer_radio.pack(side=tk.LEFT)
        self.difficulty_label = tk.Label(self.mode_frame, text="Difficulty:")
        self.difficulty_label.pack(side=tk.LEFT)
        self.difficulty_var = tk.StringVar(value="Easy")
        self.difficulty_menu = tk.OptionMenu(self.mode_frame, self.difficulty_var, "Easy", "Medium", "Hard")
        self.difficulty_menu.pack(side=tk.LEFT)
        self.reset_button = tk.Button(self.mode_frame, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(side=tk.RIGHT)
        self.all_menu = [self.player_vs_player_radio, self.player_vs_computer_radio, self.computer_vs_computer_radio, self.difficulty_menu, self.reset_button]

    def reset_game(self):
        # Εναλλαγή των παικτών σε διαδοχικούς γύρους
        # self.current_player = self.player2 if self.current_player == self.player1 else self.player1
        self.current_player = self.player1
        self.board = [" "]*9
        self.reset_board_colors()
        self.current_player_label.config(text="Player {}'s turn".format(self.current_player))
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)
        if self.game_mode.get() == "Computer vs Computer":
            self.play_computer()

    def reset_board_colors(self):
        for button in self.buttons:
            button.config(bg="SystemButtonFace")

    def update_scores(self, winner=None):
        if winner:
            self.scores[winner] += 1
        self.score_label.config(text="Player X     {} : {}     Player O".format(self.scores["X"], self.scores["O"]))

    def play(self, idx):
        if self.board[idx] == " ":
            self.board[idx] = self.current_player
            if self.current_player == self.player1:
                self.buttons[idx].config(fg="#810020")
            elif self.current_player == self.player2:
                self.buttons[idx].config(fg="#0f52ba")
            # self.buttons[idx].update()
            self.buttons[idx].config(text=self.current_player, state=tk.DISABLED,
                                     disabledforeground=self.buttons[idx].cget('fg'))
            # Απενεργοποίηση του ταμπλό μέχρι να κάνει κίνηση ο άλλος παίκτης
            for button in self.buttons + self.all_menu:
                button.config(state=tk.DISABLED)
            # Έλεγχος αν το παιχνίδι έχει τελειώσει
            if self.check_win():
                self.end_game(winner=self.current_player)
                self.update_scores(self.current_player)
                self.game_number += 1
            elif not any(c == " " for c in self.board):
                self.end_game(winner=None)
            else:
                # Εναλλαγή παίκτη και ενεργοποίηση του ταμπλό για να κάνει την κίνηση του
                self.current_player = self.player1 if self.current_player == self.player2 else self.player2
                self.master.after(500, lambda: self.current_player_label.config(
                    text="Player {}'s turn".format(self.current_player)))
                if self.game_mode.get() == "Player vs Computer" and self.current_player == self.player2:
                    # Όταν παίζει ο υπολογιστής, εισάγεται μια καθυστέρηση 1 δευτερολέπτου για την προσομοίωση
                    # ενός πιο φυσικού παιχνιδιού
                    self.master.after(1000, self.play_computer)
                else:
                    for button in self.buttons:
                        button.config(state=tk.NORMAL)

      def play_computer(self):
        if self.game_mode.get() == "Player vs Computer":
            # Απενεργοποίηση του μενού στο player vs computer και computer vs computer mode
            for button in self.all_menu:
                button.config(state=tk.DISABLED)
            player = self.player2
            print("Επίπεδο δυσκολίας: ", self.difficulty_var.get())
            empty_cells = [i for i in range(9) if self.board[i] == " "]
            if empty_cells:
                difficulty_strategies = {
                    "Easy": lambda: random.choice(empty_cells),
                    "Medium": lambda: self.computer_medium_strategy(),
                    "Hard": lambda: self.get_best_move(self.board, player)}
                strategy = difficulty_strategies.get(self.difficulty_var.get(), lambda: None)
                idx = strategy() or self.get_best_move(self.board, player)
                self.play(idx)
                # Έλεγχος αν το παιχνίδι έχει τελειώσει
                if self.check_win():
                    self.end_game(winner=player, automatic=True)
                    self.update_scores(player)
                    self.game_number += 1
                elif not empty_cells:
                    self.end_game(winner=None, automatic=True)
                else:
                    self.current_player = self.player1
        else:
            player = self.current_player
            empty_cells = [i for i in range(9) if self.board[i] == " "]
            if empty_cells:
                if random.random() < 0.5:
                    idx = random.choice(empty_cells)
                else:
                    idx = self.get_best_move(self.board, player)
                self.play(idx)
                # Έλεγχος αν το παιχνίδι έχει τελειώσει
                if self.check_win():
                    self.end_game(winner=player, automatic=True)
                elif not empty_cells:
                    self.end_game(winner=None, automatic=True)
                    # Ενεργοποίηση του ταμπλό και του μενού εφόσον το παιχνίδι έχει τελειώσει σε ισοπαλία
                    # for button in self.buttons + self.all_menu:
                        # button.config(state=tk.NORMAL)
                else:
                    # Εναλλαγή μεταξύ του παίκτη Χ και του παίκτη Ο στο computer vs computer mode
                    self.current_player = self.player1 if player == self.player2 else self.player2
                    self.master.after(1000, self.play_computer)
                    for button in self.buttons:
                        button.config(state=tk.DISABLED)

    def computer_medium_strategy(self):
        # 1. Συμπληρώνει τρίλιζα (εφόσον έχει αυτή τη δυνατότητα), ώστε να κερδίσει
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.player2
                print("Προσπάθεια για τρίλιζα στη θέση:", i)
                if self.check_win() == self.player2:
                    self.board[i] = " "
                    return i
                self.board[i] = " "

        # 2. Μπλοκάρει πιθανή τρίλιζα του αντιπάλου, εάν ο αντίπαλος μπορεί να κάνει τρίλιζα
        # στην επόμενη κίνηση του, ώστε να αποτρέψει την άμεση ήττα του
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.player1
                if self.check_win() == self.player1:
                    print("Μπλοκ πιθανής τρίλιζας του αντιπάλου για αποφυγή ήττας, στη θέση:", i)
                    self.board[i] = " "
                    if i in [0, 2, 6, 8]:
                        return i
                    break
                self.board[i] = " "

        # 3. Παίζει στην κεντρική θέση, εάν αυτή είναι ελεύθερη
        if self.board[4] == " ":
            return 4

        # 4. Παίζει σε γωνιακή θέση, εάν κάποια από αυτές είναι ελεύθερη
        corners = [0, 2, 6, 8]
        random.shuffle(corners)
        for i in corners:
            if self.board[i] == " ":
                return i

        # 5. Παίζει σε ελεύθερη θέση στο μέσο πλευράς
        sides = [1, 3, 5, 7]
        random.shuffle(sides)
        for i in sides:
            if self.board[i] == " ":
                return i

        # 6. Παίζει σε οποιαδήποτε ελεύθερη θέση
        for i in range(9):
            if self.board[i] == " ":
                return i

        # Εάν δεν υπάρχουν ελεύθερα κελιά
        return None

    def get_best_move(self, board, player):
        best_score = -1000
        best_moves = []
        for i in range(9):
            if board[i] == " ":
                board[i] = player
                score = self.minimax(board, False)
                board[i] = " "
                if score > best_score:
                    best_score = score
                    best_moves = [i]
                elif score == best_score:
                    best_moves.append(i)
        return random.choice(best_moves)

    def minimax(self, board, is_maximizing):
        winner = self.check_win(board)
        if winner:
            return -1 if winner == self.player1 else 1
        elif " " not in board:
            return 0

        scores = []
        for i in range(9):
            if board[i] == " ":
                board[i] = self.player2 if is_maximizing else self.player1
                score = self.minimax(board, not is_maximizing)
                board[i] = " "
                scores.append(score)

        return max(scores) if is_maximizing else min(scores)

    def check_win(self, board=None):
        if not board:
            board = self.board
        for combination in self.winning_combinations:
            if board[combination[0]] == board[combination[1]] == board[combination[2]] != " ":
                return board[combination[0]]
        return None

     def end_game(self, winner=None, automatic=False):
        for button in self.buttons + self.all_menu:
            button.config(state=tk.DISABLED)
        for button in self.all_menu:
            button.config(state=tk.NORMAL)
        #self.reset_button.config(state=tk.NORMAL)
        #for menu in self.buttons + self.all_menu:
            #menu.config(state=tk.NORMAL)  # Ενεργοποίηση του μενού μετά το τέλος του γύρου
        if winner:
            for combination in self.winning_combinations:
                if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != " ":
                    for idx in combination:
                        if self.board[idx] == self.player1:
                            self.buttons[idx].config(bg="#FF4D4D")
                        elif self.board[idx] == self.player2:
                            self.buttons[idx].config(bg="#3e9bed")
                    break
                    break
            if not automatic:
                messagebox.showinfo("Game Over", "Player {} wins!".format(winner))
        else:
            if not automatic:
                messagebox.showinfo("Game Over", "It's a tie!")



if __name__ == "__main__":
    root = tk.Tk()
    root.configure(background='#D9D9D9')
    root.option_add("*Font", "Consolas 12")
    root.title('Tic-Tac-Toe Game')
    game = TicTacToe(root)
    root.mainloop()

