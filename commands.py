import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from operator import itemgetter #για ταξινόμηση στοιχείων λεξικού hall_of_fame
from warnings import showwarning

nameX = 'X'
nameO = 'O'
game_round = 0

class TicTacToe(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        #self.master.grab_set()
        self.player1 = 'X'
        self.name1 = nameX
        self.player2 = 'O'
        self.name2 = nameO
        self.scores = {"X": 0, "O": 0}
        self.current_player = self.player1
        self.current_name=nameX
        self.board = [" "]*9
        self.winning_combinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.board_frame = tk.Frame(self.master)
        self.game_number = game_round
        self.buttons = []
        self.o_wins = 0
        self.x_wins = 0
        self.mode_frame = tk.Frame(self.master)
        self.setup_widgets()

    def setup_widgets(self):
        self.score_frame = tk.Frame(self.master)
        self.score_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.score_label = tk.Label(self.master, text=(f"(X) {nameX}   {self.scores['X']}  :  {self.scores['O']}   {nameO} (O)"))
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
        self.round_label.place(relx = 0.94, rely = 0.1, anchor ='ne')
        self.back_button = tk.Button(self.master, text='Back', command=player_vs_player.destroy)
        self.back_button.pack()

    def reset_game(self):
        # Εναλλαγή των παικτών σε διαδοχικούς γύρους
        if self.current_player == self.player2:
            self.current_player=self.player1
            self.current_name=self.name1
        elif self.current_player == self.player1:
            self.current_player=self.player2
            self.current_name = self.name2
        self.board = [" "] * 9
        self.reset_board_colors()
        self.current_player_label.config(text="Player {} plays".format(self.current_player))
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)

    def reset_board_colors(self):
        for button in self.buttons:
            button.config(bg="SystemButtonFace")

    def update_scores(self, winner=None):
        if winner:
            self.scores[winner] += 1
        self.score_label.config(text=(f"(X) {nameX}   {self.scores['X']}  :  {self.scores['O']}   {nameO} (O)"))
    def play(self, idx):

        global game_round

        if self.board[idx] == " ":
            self.board[idx] = self.current_player
            if self.current_player == self.player1:
                self.buttons[idx].config(fg="#810020")
            elif self.current_player == self.player2:
                self.buttons[idx].config(fg="#0f52ba")
            # self.buttons[idx].update()
            self.buttons[idx].config(text=self.current_player, state=tk.DISABLED,
                                     disabledforeground=self.buttons[idx].cget('fg'))
            winner = self.check_win()
            if winner:
                self.end_game(winner)
                self.update_scores(winner)
                self.game_number += 1
                game_round += 1
                self.reset_game()
                if self.game_number == 3:
                    if self.x_wins > self.o_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameX} wins!", parent=self.master)
                        add_winner(nameX)
                        game_round = 0
                        player_vs_player.destroy()

                    elif self.o_wins > self.x_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameO} wins!", parent=self.master)
                        add_winner(nameO)
                        game_round = 0
                        player_vs_player.destroy()
            elif " " not in self.board:
                self.end_game()
                self.update_scores(None)
                self.game_number += 1
                game_round += 1
                self.reset_game()
                if self.game_number == 3:
                    if self.x_wins > self.o_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameX} wins!", parent=self.master)
                        add_winner(nameX)
                        game_round = 0
                        player_vs_player.destroy()
                    elif self.o_wins > self.x_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameO} wins!", parent=self.master)
                        add_winner(nameO)
                        game_round = 0
                        player_vs_player.destroy()
                    elif self.x_wins == self.o_wins:
                        messagebox.showinfo("TIE!!!", message=f"None wins! It's a tie!", parent=self.master)
                        game_round = 0
                        player_vs_player.destroy()
            else:
                self.round_label.config(text="Round: {}".format(self.game_number + 1))
                if self.current_player == self.player2:
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
                        player_vs_player.destroy()
                    elif self.o_wins > self.x_wins:
                        messagebox.showinfo("Congrats", message=f"Player {nameO} wins!", parent=self.master)
                        add_winner(nameO)
                        player_vs_player.destroy()
                    elif self.x_wins == self.o_wins:
                        messagebox.showinfo("TIE!!!", message=f"None wins! It's a tie!", parent=self.master)
                        player_vs_player.destroy()



    def check_win(self, board=None):
        if not board:
            board = self.board
        for combination in self.winning_combinations:
            if board[combination[0]] == board[combination[1]] == board[combination[2]] != " ":
                return board[combination[0]]
        return None

    def end_game(self, winner=None, automatic=False):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        if winner:
            #add_winner(self.current_name)
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
                messagebox.showinfo(f"End of round {game_round+1}", message=f"None wins! It's a tie!", parent=self.master)
                self.x_wins += 0
                self.o_wins += 0


def open_credits_window():
    # Δημιουργία popup παράθυρου credits
    credits_window = tk.Toplevel()
    credits_window.title("Credits")
    credits_window.grab_set()  # για διατήριση του νέου παράθυρου στο προσκήνιο
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
                                        "in alphabetical order are:\nMallis Georgios\nPeppas Georgios\n"
                                        "Pierrakou Konstantina\nPrimpas Efstratios\nStilianou Stelios", anchor=NW,
                          font=("Helvetica", 14, 'bold'))

    # δημιουργία κουμπιού 'button_back' που κλείνει το παράθυρο credits_window
    button_back = Button(credits_window, image=Back_photo, command=credits_window.destroy)
    my_canvas.create_window(0, 420, anchor="sw", window=button_back)

    # εκτέλεση βρόγχου
    credits_window.mainloop()


def open_registration_window():

    def start_pvp():
        global player_vs_player
        global nameX
        global nameO
        nameX = entry_x.get().strip()
        nameO = entry_o.get().strip()
        if nameX == "":
            messagebox.showwarning("Warning", "Player X has no name!", parent=registration_window)

        elif nameO == "":
            messagebox.showwarning("Warning", "Player O has no name!", parent=registration_window)

        elif nameO == nameX:
            messagebox.showerror("Ident names!", "Players must have different names!", parent=registration_window)

        else:
            registration_window.destroy()
            player_vs_player = tk.Toplevel()
            player_vs_player.configure(background='#D9D9D9')
            player_vs_player.geometry("1000x700")
            player_vs_player.lift()
            # player_vs_player.attributes('-topmost',True)
            player_vs_player.grab_set()
            # root.option_add("*Font", "Consolas 12")
            player_vs_player.title('Player Vs Player')
            pvp = TicTacToe(player_vs_player)
            player_vs_player.mainloop()

    registration_window = Toplevel()
    registration_window.title("Registration Window")
    registration_window.geometry("500x300")  # διαστάσεις παράθυρου
    registration_window['bg'] = "#65a6ce"  # χρώμα παράθυρου
    registration_window.grab_set()  # διατήρηση στο προσκήνιο
    # Δημιουργία Label και EntryBox για τους παίκτες
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
    start_button = Button(registration_window, text="Start", font=('Helvetica', 20), bg="green", command=start_pvp)
    start_button.grid(row=2, columnspan=2, pady=20)


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
            fame_label = Label(fame,text="Top 10", font=('Helvetica', 20), padx=10, pady=20, width=15, background='#65a6ce')
            fame_label.pack()
            text = tk.Text(fame, font=('Helvetica', 10))
            text.configure(background='#D9D9D9')
            text.pack()
            i = 1
            for k, v in sorted(hall_of_fame.items(), key=itemgetter(1), reverse=True):
                text.insert(tk.END, f'No {i}: {k} : {v}\n')
                i += 1
                if i == 11: #εκτύπωση των 10 πρώτων
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
