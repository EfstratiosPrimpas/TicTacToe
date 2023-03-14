from  tkinter import messagebox #imports pop-up-window
import tkinter as tk


class Tic_Tac_Toe:
    def __init__(self):
        self.count = 0
        self.buttons = []
        self.player_1 = True #Player's 1 turn
        self.player_2 = False #Player's 2 turn
        self.winner = False
        self.p1="X" #P1
        self.p2="O" #P2
        self.p1_moves = [" "] * 9 #keeps track of P1's moves

        self.p2_moves = [" "] * 9  #keeps track of P2's moves

        for i in range(9): #Build the buttons and the grid
            b=tk.Button(root, text=" ", font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda idx=i: self.b_click(idx))
            b.grid(row=i // 3, column=i % 3)
            self.buttons.append(b)

        self.winning_combinations_X = ["X" , "X", "X"]
        self.winning_combinations_O = ["O", "O", "O"]

    def b_click(self, idx): # Players' movements
        i = int(idx)
        if self.player_1 == True:
            self.buttons[idx].config(text=self.p1, state=tk.DISABLED)
            self.p1_moves[i] = "X" # adds the P1's move to p1_moves
            self.player_1 = False
            self.player_2 = True # turn change
            self.count += 1
            self.check_win()
        elif self.player_2 == True:
            self.buttons[idx].config(text=self.p2, state=tk.DISABLED)
            self.p2_moves[i] = "O" # adds the P1's move to p2_moves
            self.player_1 = True
            self.player_2 = False # turn change
            self.count += 1
            self.check_win()

    def check_win(self): #checks for wins
        if self.p1_moves[0:3] == self.winning_combinations_X or self.p1_moves[3:6] == self.winning_combinations_X or self.p1_moves[6:10] == self.winning_combinations_X or [self.p1_moves[0], self.p1_moves[4], self.p1_moves[8]] == self.winning_combinations_X or [self.p1_moves[2], self.p1_moves[4], self.p1_moves[6]] == self.winning_combinations_X or [self.p1_moves[0], self.p1_moves[3], self.p1_moves[6]] == self.winning_combinations_X or [self.p1_moves[1], self.p1_moves[4], self.p1_moves[7]] == self.winning_combinations_X or [self.p1_moves[2], self.p1_moves[5], self.p1_moves[8]] == self.winning_combinations_X:
            messagebox.showinfo("Tic-Tac-Toe" , "CONGRATS, X WINS")
        elif self.p2_moves[0:3] == self.winning_combinations_O or self.p2_moves[3:6] == self.winning_combinations_O or self.p2_moves[6:10] == self.winning_combinations_O or [self.p2_moves[0], self.p2_moves[4], self.p2_moves[8]] == self.winning_combinations_O or [self.p2_moves[2], self.p2_moves[4], self.p2_moves[6]] == self.winning_combinations_O or [self.p2_moves[0], self.p2_moves[3], self.p2_moves[6]] == self.winning_combinations_O or [self.p2_moves[1], self.p2_moves[4], self.p2_moves[7]] == self.winning_combinations_O or [self.p2_moves[2], self.p2_moves[5], self.p2_moves[8]] == self.winning_combinations_O:
            messagebox.showinfo("Tic-Tac-Toe", "CONGRATS, O WINS")
        elif self.count >= 9:
            messagebox.showinfo("Tic-Tac-Toe", "IT'S A TIE")


root=tk.Tk()
root.title('Tic_Tac_Toe')
game = Tic_Tac_Toe()
root.mainloop()

