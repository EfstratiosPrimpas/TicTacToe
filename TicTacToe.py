import tkinter as tk
# Για εγκατάσταση του PIL τρέχουμε  pip install Pillow στο terminal
from PIL import Image, ImageTk

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
human_vs_human_image = Image.open("human_vs_human.png")
human_vs_human_photo = ImageTk.PhotoImage(human_vs_human_image)
human_vs_pc_image = Image.open("human_vs_pc.png")
human_vs_pc_photo = ImageTk.PhotoImage(human_vs_pc_image)
pc_vs_pc_image = Image.open("pc_vs_pc.png")
pc_vs_pc_photo = ImageTk.PhotoImage(pc_vs_pc_image)
credits_image = Image.open("credits.png")
credits_photo = ImageTk.PhotoImage(credits_image)
HallOfFame_image = Image.open("HallOfFame.png")
HallOfFame_photo = ImageTk.PhotoImage(HallOfFame_image)
Exit_image = Image.open("Exit.png")
Exit_photo = ImageTk.PhotoImage(Exit_image)

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
credits_button = tk.Button(button_frame, image=credits_photo)
credits_button.image = credits_photo
credits_button.grid(row=2, column=0, padx=5, pady=5)

hall_of_fame_button = tk.Button(button_frame, image=HallOfFame_photo)
hall_of_fame_button.image = HallOfFame_photo
hall_of_fame_button.grid(row=2, column=1, padx=5, pady=5)

exit_button = tk.Button(button_frame, image=Exit_photo)
exit_button.image = Exit_photo
exit_button.grid(row=2, column=2, padx=5, pady=5)

# Τρέχει την κύρια λούπα
root.mainloop()