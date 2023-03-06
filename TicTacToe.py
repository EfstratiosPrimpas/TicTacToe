import tkinter as tk
from tkinter import *
# Για εγκατάσταση του PIL τρέχουμε  pip install Pillow στο terminal
from PIL import Image, ImageTk


# Συνάρτηση που καλείται μόλις πατηθεί το κουμπί "Credits"
def open_credits_window():
    # Δημιουργία popup παράθυρου credits
    credits_window = tk.Toplevel()
    credits_window.title("Credits")
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
human_vs_human_button = tk.Button(button_frame, image=human_vs_human_photo)
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
