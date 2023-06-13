import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from operator import itemgetter  # για ταξινόμηση στοιχείων λεξικού hall_of_fame
from warnings import showwarning
import random

nameX = 'X'
nameO = 'O'
game_round = 0
difficulty = "m"
entry_x = None
entry_o = None


# Κύρια κλάση του παιχνιδιού
class TicTacToe(tk.Frame):
    def __init__(self, master, game_mode_var, difficulty_var):
        super().__init__(master)
        self.master = master
        self.player1 = 'X'
        self.name1 = nameX
        self.player2 = 'O'
        self.name2 = nameO
        self.scores = {"X": 0, "O": 0}
        self.current_player = self.player1
        self.current_name = nameX
        self.board = [" "]*9
        self.winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]] #Νικητηριοι συνδυασμοί
        self.board_frame = tk.Frame(self.master)
        self.game_number = game_round
        self.buttons = []
        self.o_wins = 0 #Νίκες παίκτη Ο
        self.x_wins = 0 #Νίκες παίκτη Χ
        self.mode_frame = tk.Frame(self.master)
        self.setup_widgets()
        self.game_mode_var = game_mode_var  # Μεταβλητή για τις διάφορες λειτουργίες του παιχνιδιού
        self.difficulty_var = difficulty_var  # Μεταβλητή για το επίπεδο δυσκολίας

    def setup_widgets(self):
        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.score_label = tk.Label(self.master, text=f"(X) {nameX}   {self.scores['X']}  :  {self.scores['O']}   {nameO} (O)")
        self.score_label.pack(side=tk.TOP, pady=10)
        self.master.update_idletasks()
        self.score_label.place(relx=0.5, y=0.5, anchor=tk.N)
        self.board_frame = tk.Frame(self.master, highlightbackground='#000000', bd=2)
        self.board_frame.pack(padx=10, pady=10)
        # Δημιουργία των κουμπιών του ταμπλώ
        self.buttons = []
        for i in range(9):
            button = tk.Button(self.board_frame, text="", width=5, height=2, font=("Helvetica", 40, "bold"),
                               command=lambda idx=i: self.play(idx))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)
        # Δημιουργία του label που εμφανίζει ποιος είναι ο ενεργός παίκτης
        self.current_player_label = tk.Label(self.master, text="Player {} plays".format(self.current_player), bd=3,
                                             relief=tk.FLAT, anchor=tk.E, bg="#bdcdff", padx=20, pady=6,
                                             font=("Consolas", 12, "bold"), highlightthickness=2,
                                             highlightbackground="blue")
        self.current_player_label.place(relx=0.97, rely=0.2, anchor=tk.E)
        self.mode_frame = tk.Frame(self.master)
        self.mode_frame.pack(padx=200, pady=5)
        self.reset_button = tk.Button(self.mode_frame, text="Reset Game", command=self.reset_game)
        self.reset_button.pack(side=tk.RIGHT)
        self.round_label = tk.Label(self.master, text=f'Round: {game_round+1}', bd=3,
                                    relief=tk.FLAT, anchor=tk.E, bg="#bdcdff", padx=20, pady=6,
                                    font=("Consolas", 12, "bold"), highlightthickness=2,
                                    highlightbackground="blue")
        self.round_label.place(relx=0.94, rely=0.1, anchor='ne')
        self.back_button = tk.Button(self, text='Back', command=self.destroy_game)
        self.back_button.pack()

    # Μέθοδος για το κλείσιμο του παιχνιδιού
    def destroy_game(self):
        global game_round
        game_round = 0
        self.master.destroy()

    def reset_game(self):
        # Εναλλαγή των παικτών σε διαδοχικούς γύρους

        if self.game_mode_var == "Player vs Computer" or self.game_mode_var == "Player vs Player" or self.game_mode_var == "Computer vs Computer":
            if self.game_number == 1:
                # Ο παίκτης 2 (Ο) παίζει πρώτος στον 2ο γύρο
                self.current_player = self.player2
                self.current_name = self.name2
            else:
                # Εναλλαγή των παικτών για τους επόμενους γύρους
                if self.current_player == self.player1:
                    self.current_player = self.player2
                    self.current_name = self.name2
                else:
                    self.current_player = self.player1
                    self.current_name = self.name1

        # Εμφάνιση του ταμπλώ και των κουμπιών μετά από την επανεκκίνηση κάθε γύρου
        self.board = [" "] * 9
        self.reset_board_colors()
        self.current_player_label.config(text="Player {} plays".format(self.current_player))
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)

        if self.game_mode_var == "Player vs Computer" and self.current_player == self.player2:
            if self.game_number == 1:
                self.play_computer()

    # Μέθοδος για την επαναφορά των κουμπιών του ταμπλώ στην αρχική κατάσταση τους
    def reset_board_colors(self):
        for button in self.buttons:
            button.config(bg="SystemButtonFace")

    # Μέθοδος για την ενημέρωση του σκορ
    def update_scores(self, winner=None):
        if winner:
            self.scores[winner] += 1
        self.score_label.config(text=f"(X) {nameX}   {self.scores['X']}  :  {self.scores['O']}   {nameO} (O)")

    def play(self, idx):
        global game_round
        if self.board[idx] == " ":
            self.board[idx] = self.current_player
            if self.current_player == self.player1: #Τοποθέτηση ονόματος σε παίκτη Χ
                self.current_name = nameX
                self.buttons[idx].config(fg="#810020")
            elif self.current_player == self.player2:
                self.current_name = nameO #Τοποθέτηση ονόματος σε παίκτη Ο
                self.buttons[idx].config(fg="#0f52ba")
            self.buttons[idx].config(text=self.current_player, state=tk.DISABLED,
                                     disabledforeground=self.buttons[idx].cget('fg'))
            for button in self.buttons:
                button.config(state=tk.DISABLED)
            winner = self.check_win()
            if winner: #Εαν βρεθεί νικητής
                self.end_game(winner)
                self.update_scores(winner)
                self.game_number += 1
                game_round += 1
                self.reset_game()
                if self.game_number == 3: #Αν ολοκληρωθούν τρείς γύροι
                    if self.x_wins > self.o_wins: #Σύγκριση νικών
                        messagebox.showinfo("Congrats", message=f"Player {nameX} wins!", parent=self.master)
                        add_winner(nameX)
                        game_round = 0 #Μηδενισμός γύρων

                        self.destroy_game()
                    elif self.o_wins > self.x_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameO} wins!", parent=self.master)
                        add_winner(nameO)
                        game_round = 0

                        self.destroy_game()
                    elif self.x_wins == self.o_wins:
                        messagebox.showinfo("TIE!!!", message=f"None wins! It's a tie!", parent=self.master)
                        game_round = 0

                        self.destroy_game()
            elif " " not in self.board: #Εάν δεν υπάρχουν κενές θέσεις
                self.end_game()
                self.update_scores(None)
                self.game_number += 1
                game_round += 1
                self.reset_game()
                if self.game_number == 3: #Αν ολοκληρωθούν τρείς γύροι και δεν υπάρχει κενή θέση
                    if self.x_wins > self.o_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameX} wins!", parent=self.master)
                        add_winner(nameX)
                        game_round = 0
                        self.destroy_game()
                    elif self.o_wins > self.x_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameO} wins!", parent=self.master)
                        add_winner(nameO)
                        game_round = 0
                        self.destroy_game()
                    elif self.x_wins == self.o_wins:
                        messagebox.showinfo("TIE!!!", message=f"None wins! It's a tie!", parent=self.master)
                        game_round = 0
                        self.destroy_game()
            elif self.round_label.config(text="Round: {}".format(self.game_number + 1)): #Προσαύξηση γύρου σε αντίστοιχο label
                if self.current_player == self.player2: #Εναλλαγή παικτών
                    self.current_player = self.player1
                    self.current_name = self.name1
                elif self.current_player == self.player1:
                    self.current_player = self.player2
                    self.current_name = self.name2
                self.current_player_label.config(text="Player {} plays".format(self.current_player))

                if self.game_number == 3:  
                    if self.x_wins > self.o_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameX} wins!", parent=self.master)
                        add_winner(nameX)
                        self.destroy_game()
                    elif self.o_wins > self.x_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameO} wins!", parent=self.master)
                        add_winner(nameO)
                        self.destroy_game()
                    elif self.x_wins == self.o_wins:
                        messagebox.showinfo("TIE!!!", message=f"No one wins! It's a tie!", parent=self.master)
                        self.destroy_game()
            else:
                # Εναλλαγή παίκτη
                self.current_player = self.player1 if self.current_player == self.player2 else self.player2
                self.master.after(500, lambda: self.current_player_label.config(
                    text="Player {}'s turn".format(self.current_player)))
                if self.game_mode_var == "Player vs Computer" and self.current_player == self.player2:
                    # Όταν παίζει ο υπολογιστής, εισάγεται μια καθυστέρηση 1 δευτερολέπτου για την προσομοίωση
                    # ενός πιο φυσικού παιχνιδιού
                    self.master.after(1000, self.play_computer)
                else:
                    for button in self.buttons:  # Ενεργοποίηση των κουμπιών του ταμπλώ
                        button.config(state=tk.NORMAL)

    def start_computer_play(self):
        self.game_mode_var = "Computer vs Computer"
        self.play_computer()

    # Μέθοδος για τη συμπεριφορά του αυτόματου παίκτη
    def play_computer(self):
        global game_round
        print("Playing computer in mode:", self.game_mode_var)
        if self.game_mode_var == "Player vs Computer":
            player = self.player2
            print("Επίπεδο δυσκολίας: ", self.difficulty_var)
            empty_cells = [i for i in range(9) if self.board[i] == " "]
            if empty_cells:
                # Στρατηγικές του αυτόματου παίκτη
                difficulty_strategies = {
                    "Easy": lambda: random.choice(empty_cells),
                    "Medium": lambda: self.computer_medium_strategy(),
                    "Hard": lambda: self.get_best_move(self.board, player)}
                strategy = difficulty_strategies.get(self.difficulty_var, lambda: None)
                idx = strategy() or self.get_best_move(self.board, player)
                self.play(idx)
                # Έλεγχος αν το παιχνίδι έχει τελειώσει
                if self.check_win():
                    self.end_game(winner=player, automatic=True)
                    self.update_scores(player)
                    self.game_number += 1
                    game_round += 1
                    self.reset_game()
                elif not empty_cells:  # Έλεγχος εάν δεν υπάρχουν ελεύθερα κελιά
                    self.end_game(winner=None, automatic=True)
                    self.update_scores(player)
                    self.game_number += 1
                    game_round += 1
                    self.reset_game()
                else:
                    self.current_player = self.player1
        # Λογική για το mode Computer vs Computer
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
                    self.update_scores(player)
                    self.game_number += 1
                    game_round += 1
                    self.reset_game()
                elif not empty_cells:  # Έλεγχος εάν δεν υπάρχουν ελεύθερα κελιά
                    self.end_game(winner=None, automatic=True)
                    self.update_scores(player)
                    self.game_number += 1
                    game_round += 1
                    self.reset_game()
                else:
                    # Εναλλαγή μεταξύ του παίκτη Χ και του παίκτη Ο στο computer vs computer mode
                    print("Playing computer in mode:", self.game_mode_var)
                    self.current_player = self.player1 if player == self.player2 else self.player2
                    # Όταν παίζει ο υπολογιστής, εισάγεται μια καθυστέρηση 1 δευτερολέπτου για την προσομοίωση
                    # ενός πιο φυσικού παιχνιδιού
                    self.master.after(1000, self.play_computer)
                    for button in self.buttons:
                        button.config(state=tk.DISABLED)

    # Μέθοδος για τη στρατηγική medium difficulty του αυτόματου παίκτη
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

    # Μέθοδος για την επιλογή της καλύτερης κίνησης του αυτόματου παίκτη (hard difficulty)
    def get_best_move(self, board, player):
        best_score = -1000  # Αρχικοποίηση του καλύτερου σκορ σε πολύ μικρή τιμή
        best_moves = []  # Αρχικοποίηση της λίστας των καλύτερων κινήσεων
        for i in range(9):
            if board[i] == " ":
                board[i] = player  # Κάνει μια υποθετική κίνηση
                score = self.minimax(board, False)  # Υπολογισμός της βαθμολογίας χρησιμοποιώντας τον αλγόριθμο minimax
                board[i] = " "  # Αναιρεί την υποθετική κίνηση
                if score > best_score:  # Εάν η βαθμολογία είναι καλύτερη από την τρέχουσα καλύτερη βαθμολογία
                    best_score = score  # Ενημέρωση της καλύτερης βαθμολογίας
                    best_moves = [i]    # Αντικατάσταση της λίστας με τις καλύτερες κινήσεις με μια νέα κίνηση
                elif score == best_score:  # Εάν η βαθμολογία είναι ίση με την τρέχουσα καλύτερη βαθμολογία
                    best_moves.append(i)   # Προσθέτει την κίνηση στη λίστα με τις καλύτερες κινήσεις
        return random.choice(best_moves)  # Επιλέγει μια τυχαία κίνηση από τη λίστα με τις καλύτερες κινήσεις

    # Μέθοδος minimax η οποία χρησιμοποιεί τον αλγόριθμο minimax, για να μεγιστοποιήσει τις πιθανότητες νίκης
    # του αυτόματου παίκτη, ελαχιστοποιώντας ταυτόχρονα τις πιθανότητες νίκης του αντιπάλου.
    def minimax(self, board, is_maximizing):
        winner = self.check_win(board)  # Έλεγχος για νικητή
        if winner:
            return -1 if winner == self.player1 else 1
        elif " " not in board:
            return 0

        scores = []  # Λίστα για την αποθήκευση βαθμολογίας για κάθε πιθανή κίνηση
        for i in range(9):
            if board[i] == " ":
                board[i] = self.player2 if is_maximizing else self.player1  # Κάνει μια υποθετική κίνηση
                score = self.minimax(board, not is_maximizing)  # Αναδρομική κλήση στη minimax για την επόμενη κίνηση
                board[i] = " "  # Αναιρεί την υποθετική κίνηση
                scores.append(score)  # Αποθηκεύει το σκορ της κίνησης

        return max(scores) if is_maximizing else min(scores)

    # Μέθοδος που ελέγχει την περίπτωση νίκης σε ένα γύρο.
    def check_win(self, board=None):
        if not board:
            board = self.board
        for combination in self.winning_combinations:
            if board[combination[0]] == board[combination[1]] == board[combination[2]] != " ":
                return board[combination[0]]
        return None

    # Μέθοδος που ελέγχει εάν το παιχνίδι έχει τελειώσει
    def end_game(self, winner=None, automatic=False):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        if winner:
            # Έλεγχος των πιθανών συνδυασμών
            for combination in self.winning_combinations:
                if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != " ":
                    for idx in combination:
                        if self.board[idx] == self.player1:
                            self.buttons[idx].config(bg="#FF4D4D")
                            self.x_wins += 1
                        elif self.board[idx] == self.player2:
                            self.buttons[idx].config(bg="#008ECC")
                            self.o_wins += 1
                    break
            if not automatic:
                messagebox.showinfo(f"End of round {game_round+1}", message=f"Player {self.current_name} wins!", parent=self.master)
        else:
            if not automatic:
                messagebox.showinfo(f"End of round {game_round+1}", message=f"No one wins! It's a tie!", parent=self.master)
                self.x_wins += 0
                self.o_wins += 0


def open_credits_window():
    # Δημιουργία popup παράθυρου credits
    credits_window = tk.Toplevel()
    credits_window.title("Credits")
    credits_window.grab_set()  # για διατήρηση του νέου παράθυρου στο προσκήνιο
    credits_window.geometry("700x420+100+100")  # διαστάσεις και θέση παράθυρου 'credits_window' στην οθόνη

    # Φόρτωση της εικόνας φόντου
    bg = PhotoImage(file=r"./images/python.png")
    # δημιουργία αντικείμενου 'canvas' στο 'credits_window' με συγκεκριμένες διαστάσεις
    my_canvas = Canvas(credits_window, width=500, height=420)
    # τοποθέτηση του widget 'my_canvas' σε όλο το παράθυρο
    my_canvas.pack(fill="both", expand=True)
    # τοποθέτηση εικόνας bg στο παράθυρο με αγκίστρωση πάνω αριστερά
    my_canvas.create_image(0, 0, image=bg, anchor="nw")
    Back_photo = ImageTk.PhotoImage(Image.open("images/back.png"))

    # Δημιουργία κειμένου στο my_canvas
    my_canvas.create_text(290, 10, text="TicTacToe Project\n\nThis project was created as part\nof the PLIPRO "
                                        "thematic unit\nof the Hellenic Open University.\n\nCreators "
                                        "in alphabetical order are:\nPeppas Georgios\n" "Pierrakou Konstantina\n"
                                        "Primpas Efstratios\nStylianou Stelios", anchor=NW,
                                        font=("Helvetica", 14, 'bold'))

    # δημιουργία κουμπιού 'button_back' που κλείνει το παράθυρο credits_window
    button_back = Button(credits_window, image=Back_photo, command=credits_window.destroy)
    my_canvas.create_window(0, 420, anchor="sw", window=button_back)

    # εκτέλεση βρόγχου
    credits_window.mainloop()


def on_closing():
    pass


def open_registration_window(mode, game_mode_var):
    game_mode_var.set(mode)
    print("Selected game mode:", game_mode_var.get())
    registration_window = Toplevel()
    registration_window.title("Registration Window")
    registration_window.geometry("500x380")  # dimensions of the window
    registration_window['bg'] = "#65a6ce"  # window color
    registration_window.grab_set()  # keep the window in the foreground

    # Δημιουργία ετικετών και χώρου για την εισαγωγή ονομάτων των παικτών
    label_x = Label(registration_window, text="Name of player X", font=('Helvetica', 15), padx=10, pady=20, width=15,
                    bg="#d05f5f")
    label_x.grid(row=0, column=0, pady=5, padx=5)
    label_o = Label(registration_window, text="Name of player O", font=('Helvetica', 15), padx=10, pady=20, width=15,
                    bg="#44c9b2")
    label_o.grid(row=1, column=0, pady=20, padx=5)
    entry_x = Entry(registration_window, font=('Helvetica', 15), width=25)
    entry_x.grid(row=0, column=1)
    entry_o = Entry(registration_window, font=('Helvetica', 15), width=25)
    entry_o.grid(row=1, column=1)
    # Τροποποίηση του registration window στην περίπτωση επιλογής του Player vs Computer mode
    if mode == "Player vs Computer":
        entry_o.insert(0, "Computer")
        entry_o.configure(state='readonly')
        # Δημιουργία κουμπιού και μενού για την επιλογή επιπέδου δυσκολίας
        label_difficulty = Label(registration_window, text="Select Difficulty", font=('Helvetica', 15, 'bold'), padx=10, pady=20,
                                 width=15, bg="#65a6ce")
        label_difficulty.grid(row=2, column=0)
        difficulty_var = StringVar(registration_window)
        difficulty_var.set("Easy")  # Αρχική τιμή του επιπέδου δυσκολίας
        difficulty_menu = OptionMenu(registration_window, difficulty_var, "Easy", "Medium", "Hard")
        difficulty_menu.grid(row=3, column=0)
    # Τροποποίηση του registration window στην περίπτωση επιλογής του Computer vs Computer mode
    elif mode == "Computer vs Computer":
        entry_x.insert(0, "Computer1")
        entry_x.configure(state='readonly')
        entry_o.insert(0, "Computer2")
        entry_o.configure(state='readonly')

    # Μέθοδος για την εκκίνηση του παιχνιδιού βάσει των επιλογών
    def start_game(registration_window, game_mode_var, difficulty_var=None):
        global nameX
        global nameO
        nameX = entry_x.get().strip()
        nameO = entry_o.get().strip()
        # Αμυντικός προγραμματισμός για σωστή εισαγωγή ονομάτων
        if nameX == "":
            messagebox.showwarning("Warning", "Player X has no name!")
        elif nameO == "":
            messagebox.showwarning("Warning", "Player O has no name!")
        elif nameO.lower() == nameX.lower():
            messagebox.showerror("Identical names!", "Players must have different names!")
        else:
            print("Starting game with mode:", game_mode_var.get())
            if game_mode_var.get() == "Player vs Computer":
                print("Selected difficulty:", difficulty_var.get())
            registration_window.destroy()
            root = tk.Toplevel()
            root.geometry("1000x700")
            root.title('Tic Tac Toe')
            root.protocol("WM_DELETE_WINDOW", on_closing)
            game_instance = TicTacToe(root, game_mode_var.get(), difficulty_var.get() if difficulty_var else None)
            game_instance.pack()
            if game_mode_var.get() == "Computer vs Computer":
                game_instance.start_computer_play()
            root.grab_set()
            root.mainloop()
    # Κουμπί εκκίνησης του παιχνιδιού με τις διάφορες επιλογές
    start_button = Button(registration_window, text="Start", font=('Helvetica', 20), bg="green",
                          command=lambda: start_game(registration_window, game_mode_var,
                          difficulty_var if mode == "Player vs Computer" else None))
    start_button.grid(row=3, column=1)


def open_hall_of_fame():
    try:
        with open("hall_of_fame.json") as f:
            hall_of_fame = json.load(f)
            fame = tk.Toplevel()
            fame.iconbitmap("images/crown.ico")
            fame.configure(background='#65a6ce')
            fame.geometry("800x500")
            fame.lift()
            fame.grab_set()
            fame.title('Hall Of Fame')
            fame_label = Label(fame, text="Top 10", font=('Helvetica', 20), padx=10, pady=20, width=15, background='#65a6ce')
            fame_label.pack()
            text = tk.Text(fame, font=('Helvetica', 10))
            text.configure(background='#D9D9D9')
            text.pack()
            i = 1
            for k, v in sorted(hall_of_fame.items(), key=itemgetter(1), reverse=True):
                text.insert(tk.END, f'No {i}: {k} : {v}\n')
                i += 1
                if i == 11:  # Εκτύπωση των 10 πρώτων σκόρερ
                    break
    except FileNotFoundError:
        messagebox.showerror("Invalid action!", "There are no winners yet!")


def add_winner(name):
    try:
        with open("hall_of_fame.json") as f:
            hall_of_fame = json.load(f)
            if name in hall_of_fame:
                hall_of_fame[name] += 1
                with open("hall_of_fame.json", "w") as f:
                    json.dump(hall_of_fame, f)
            else:
                hall_of_fame[name] = 1
                with open("hall_of_fame.json", "w") as f:
                    json.dump(hall_of_fame, f)

    except FileNotFoundError:
        hall_of_fame = {name: 1}
        with open("hall_of_fame.json", "w") as f:
            json.dump(hall_of_fame, f)
