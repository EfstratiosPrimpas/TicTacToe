import tkinter as tk
import tkinter as tk
from tkinter import *
# Για εγκατάσταση του PIL τρέχουμε  pip install Pillow στο terminal ή python.exe -m pip install --upgrade pip
from PIL import Image, ImageTk
from tkinter import messagebox


# GLOBAL ΜΕΤΑΒΛΗΤΕΣ ΟΝΟΜΑΤΩΝ ΠΑΙΚΤΩΝ
nameX = "X"
nameO = "O"


# Συνάρτηση που καλείται μόλις πατηθεί το κουμπί "Credits"
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
    global nameX
    global nameO

    def start_pvp():
        nameX = entry_x.get().strip()
        nameO = entry_o.get().strip()
        if nameX=="":
            messagebox.showwarning("Warning","Player X has no name!",parent=registration_window)

        elif nameO=="":
            messagebox.showwarning("Warning","Player O has no name!",parent=registration_window)

        else:
            registration_window.destroy()
            class Tic_Tac_Toe:

                def __init__(self):
                    self.count = 0
                    self.buttons = []
                    self.player_1 = True  # Player's 1 turn
                    self.player_2 = False  # Player's 2 turn
                    self.winner = False
                    self.p1 = "X"  # P1
                    self.p2 = "O"  # P2
                    self.p1_moves = [" "] * 9  # keeps track of P1's moves

                    self.p2_moves = [" "] * 9  # keeps track of P2's moves

                    for i in range(9):  # Build the buttons and the grid
                        b = tk.Button(pvp, text=" ", font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace",
                                      command=lambda idx=i: self.b_click(idx))
                        b.grid(row=i // 3, column=i % 3)
                        self.buttons.append(b)

                    self.winning_combinations_X = ["X", "X", "X"]
                    self.winning_combinations_O = ["O", "O", "O"]

                def b_click(self, idx):  # Players' movements
                    i = int(idx)
                    if self.player_1 == True:
                        self.buttons[idx].config(text=self.p1, state=tk.DISABLED)
                        self.p1_moves[i] = "X"  # adds the P1's move to p1_moves
                        self.player_1 = False
                        self.player_2 = True  # turn change
                        self.count += 1
                        self.check_win()
                    elif self.player_2 == True:
                        self.buttons[idx].config(text=self.p2, state=tk.DISABLED)
                        self.p2_moves[i] = "O"  # adds the P1's move to p2_moves
                        self.player_1 = True
                        self.player_2 = False  # turn change
                        self.count += 1
                        self.check_win()

                def check_win(self):  # checks for wins
                    if self.p1_moves[0:3] == self.winning_combinations_X or self.p1_moves[
                                                                            3:6] == self.winning_combinations_X or self.p1_moves[
                                                                                                                   6:9] == self.winning_combinations_X or [
                        self.p1_moves[0], self.p1_moves[4], self.p1_moves[8]] == self.winning_combinations_X or [
                        self.p1_moves[2], self.p1_moves[4], self.p1_moves[6]] == self.winning_combinations_X or [
                        self.p1_moves[0], self.p1_moves[3], self.p1_moves[6]] == self.winning_combinations_X or [
                        self.p1_moves[1], self.p1_moves[4], self.p1_moves[7]] == self.winning_combinations_X or [
                        self.p1_moves[2], self.p1_moves[5], self.p1_moves[8]] == self.winning_combinations_X:
                        self.disable_buttons()
                        messagebox.showinfo("Tic-Tac-Toe", "CONGRATS, X WINS",parent=pvp)

                    elif self.p2_moves[0:3] == self.winning_combinations_O or self.p2_moves[
                                                                              3:6] == self.winning_combinations_O or self.p2_moves[
                                                                                                                     6:9] == self.winning_combinations_O or [
                        self.p2_moves[0], self.p2_moves[4], self.p2_moves[8]] == self.winning_combinations_O or [
                        self.p2_moves[2], self.p2_moves[4], self.p2_moves[6]] == self.winning_combinations_O or [
                        self.p2_moves[0], self.p2_moves[3], self.p2_moves[6]] == self.winning_combinations_O or [
                        self.p2_moves[1], self.p2_moves[4], self.p2_moves[7]] == self.winning_combinations_O or [
                        self.p2_moves[2], self.p2_moves[5], self.p2_moves[8]] == self.winning_combinations_O:
                        self.disable_buttons()
                        messagebox.showinfo("Tic-Tac-Toe", "CONGRATS, O WINS",parent=pvp)

                    elif self.count >= 9:
                        self.disable_buttons()
                        messagebox.showinfo("Tic-Tac-Toe", "IT'S A TIE",parent=pvp)


                def disable_buttons(self):
                    for button in self.buttons:
                        button.config(state=tk.DISABLED)


            pvp=Toplevel()
            pvp.grab_set()
            Tic_Tac_Toe()
            pvp.mainloop()

        #label = Label(registration_window,text=nameX)
        #label.grid(row=3)
        #label = Label(registration_window, text=nameO)
        #label.grid(row=4)
    registration_window=Toplevel()
    registration_window.title("Registration Window")
    registration_window.geometry("500x300")  # διαστάσεις παράθυρου
    registration_window['bg'] = "#65a6ce"  # χρώμα παράθυρου
    registration_window.grab_set()  # διατήρηση στο προσκήνιο
    # Δημιουργία Label και EntryBox για τους παίκτες
    label_x=Label(registration_window,text="Name of player X",font=('Helvetica',15),padx=10,pady=20,width=15,bg="#d05f5f")
    label_x.grid(row=0,column=0,pady=5,padx=5)
    label_o = Label(registration_window, text="Name of player O", font=('Helvetica', 15), padx=10, pady=20,width=15,bg="#44c9b2")
    label_o.grid(row=1, column=0,pady=20,padx=5)
    entry_x=Entry(registration_window,font=('Helvetica', 15),width=25)
    entry_x.grid(row=0,column=1)
    entry_o = Entry(registration_window, font=('Helvetica', 15), width=25)
    entry_o.grid(row=1, column=1)
    start_button=Button(registration_window,text="Start",font=('Helvetica',20),bg="green",command=start_pvp)
    start_button.grid(row=2,columnspan=2,pady=20)


# Δημιουργία του αρχικού παραθύρου
root = tk.Tk()
root.title("Tic Tac Toe")

# Δημιουργία της επικεφαλίδας
header_label = tk.Label(root, text="Welcome to Tic Tac Toe\nChoose an option to begin", font=("Helvetica", 16), pady=10)
header_label.pack()

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack()

# Φόρτωση όλων των εικονιδίων για τα κουμπιά
human_vs_human_image = Image.open(r"./images/human_vs_human.png")
human_vs_human_photo = ImageTk.PhotoImage(human_vs_human_image)
human_vs_pc_image = Image.open(r"./images/human_vs_pc.png")
human_vs_pc_photo = ImageTk.PhotoImage(human_vs_pc_image)
pc_vs_pc_image = Image.open(r"./images/pc_vs_pc.png")
pc_vs_pc_photo = ImageTk.PhotoImage(pc_vs_pc_image)
credits_image = Image.open(r"./images/credits.png")
credits_photo = ImageTk.PhotoImage(credits_image)
HallOfFame_image = Image.open(r"./images/HallOfFame.png")
HallOfFame_photo = ImageTk.PhotoImage(HallOfFame_image)
Exit_image = Image.open(r"./images/Exit.png")
Exit_photo = ImageTk.PhotoImage(Exit_image)
Back_image = Image.open(r"./images/back.png")
Back_photo = ImageTk.PhotoImage(Back_image)

# Δημιουργία των 3 διαφορετικών κουμπιών με τύπο αντιπάλων / οριζόντια τοποθέτηση
human_vs_human_button = tk.Button(button_frame, image=human_vs_human_photo, command=open_registration_window)
human_vs_human_button.image = human_vs_human_photo
human_vs_human_button.grid(row=0, column=0, padx=5, pady=5)

human_vs_human_label = tk.Label(button_frame, text="Human Vs Human")
human_vs_human_label.grid(row=1, column=0)

human_vs_pc_button = tk.Button(button_frame, image=human_vs_pc_photo)
human_vs_pc_button.image = human_vs_pc_photo
human_vs_pc_button.grid(row=0, column=1, padx=5, pady=5)

human_vs_pc_label = tk.Label(button_frame, text="Human Vs PC")
human_vs_pc_label.grid(row=1, column=1)

pc_vs_pc_button = tk.Button(button_frame, image=pc_vs_pc_photo)
pc_vs_pc_button.image = pc_vs_pc_photo
pc_vs_pc_button.grid(row=0, column=2, padx=5, pady=5)

pc_vs_pc_label = tk.Label(button_frame, text="PC Vs PC")
pc_vs_pc_label.grid(row=1, column=2)

# Δημιουργία των κουμπιών Credits, Hall of Fame, Exit / οριζόντια τοποθέτηση
credits_button = tk.Button(button_frame, image=credits_photo, command=open_credits_window)
credits_button.image = credits_photo
credits_button.grid(row=2, column=0, padx=5, pady=20)

hall_of_fame_button = tk.Button(button_frame, image=HallOfFame_photo)
hall_of_fame_button.image = HallOfFame_photo
hall_of_fame_button.grid(row=2, column=1, padx=5, pady=20)

exit_button = tk.Button(button_frame, image=Exit_photo, command=root.destroy)
exit_button.image = Exit_photo
exit_button.grid(row=2, column=2, padx=5, pady=20)

# Τρέχει την κύρια λούπα
root.mainloop()