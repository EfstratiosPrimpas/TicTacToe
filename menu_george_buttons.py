import tkinter as tk
# Για εγκατάσταση του PIL τρέχουμε  pip install Pillow στο terminal
from PIL import Image, ImageTk
from commands import *


# Δημιουργία του αρχικού παραθύρου
root = tk.Tk()
root.title("Tic Tac Toe")
root.iconbitmap("images/tic tac toe icon.ico")
root.configure(background='#66b3ff')


# Δημιουργία της επικεφαλίδας
header_label = tk.Label(root, text="Welcome to Tic Tac Toe\nChoose an option to begin", font=("Helvetica", 16), pady=10, background='#66b3ff')
header_label.pack()

# Create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.configure(background='#66b3ff')
button_frame.pack()

# Φόρτωση όλων των εικονιδίων για τα κουμπιά
human_vs_human_photo = ImageTk.PhotoImage(Image.open("images/human_vs_human.png"))
human_vs_pc_photo = ImageTk.PhotoImage(Image.open("images/human_vs_pc.png"))
pc_vs_pc_photo = ImageTk.PhotoImage(Image.open("images/pc_vs_pc.png"))
credits_photo = ImageTk.PhotoImage(Image.open("images/credits.png"))
HallOfFame_photo = ImageTk.PhotoImage(Image.open("images/HallOfFame.png"))
Exit_photo = ImageTk.PhotoImage(Image.open("images/Exit.png"))

# Δημιουργία των 3 διαφορετικών κουμπιών με τύπο αντιπάλων / οριζόντια τοποθέτηση
human_vs_human_button = tk.Button(button_frame, image=human_vs_human_photo, command=open_registration_window, activebackground= "red", bg="#66b3ff", cursor="gumby", border=0)
human_vs_human_button.image = human_vs_human_photo
human_vs_human_button.grid(row=0, column=0, padx=5, pady=5)

human_vs_human_label = tk.Label(button_frame, text="Human Vs Human", background='#66b3ff')
human_vs_human_label.grid(row=1, column=0)

human_vs_pc_button = tk.Button(button_frame, image=human_vs_pc_photo, activebackground= "red", bg="#66b3ff", cursor="pirate", border=0)
human_vs_pc_button.grid(row=0, column=1, padx=5, pady=5)

human_vs_pc_label = tk.Label(button_frame, text="Human Vs PC", background='#66b3ff' )
human_vs_pc_label.grid(row=1, column=1)

pc_vs_pc_button = tk.Button(button_frame, image=pc_vs_pc_photo, activebackground= "red", bg="#66b3ff", cursor="coffee_mug", border=0)
pc_vs_pc_button.grid(row=0, column=2, padx=5, pady=5)

pc_vs_pc_label = tk.Label(button_frame, text="PC Vs PC", background='#66b3ff')
pc_vs_pc_label.grid(row=1, column=2)

# Δημιουργία των κουμπιών Credits, Hall of Fame, Exit / οριζόντια τοποθέτηση
credits_button = tk.Button(button_frame, image=credits_photo, command=open_credits_window, activebackground= "red", bg="#66b3ff", cursor="hand2", border=0)
credits_button.grid(row=2, column=0, padx=5, pady=20)

hall_of_fame_button = tk.Button(button_frame, image=HallOfFame_photo, activebackground= "red", bg="#66b3ff", cursor="hand2", border=0, command=open_hall_of_fame)
hall_of_fame_button.grid(row=2, column=1, padx=5, pady=20)

exit_button = tk.Button(button_frame, image=Exit_photo, command=root.destroy, activebackground= "red", bg="#66b3ff", cursor="hand2", border=0)
exit_button.grid(row=2, column=2, padx=5, pady=20)

# Τρέχει την κύρια λούπα
root.mainloop()
