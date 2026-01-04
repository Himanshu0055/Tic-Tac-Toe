import customtkinter as ctk
import random
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------- CONFIG ----------------
COLOR_X = "#4da6ff"
COLOR_O = "#ff4d4d"

board = [" "] * 9
buttons = []
current_player = "X"
game_mode = "FRIEND"

x_score = 0
o_score = 0
draw_score = 0

# ---------------- LOGIC ----------------
def check_winner(p):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    return any(board[a] == board[b] == board[c] == p for a,b,c in wins)

def ai_move():
    empty = [i for i in range(9) if board[i] == " "]
    return random.choice(empty)

def update_score():
    score_label.configure(
        text=f"X : {x_score}    O : {o_score}    Draws : {draw_score}"
    )

# ---------------- GAME FLOW ----------------
def on_click(i):
    global current_player, x_score, o_score, draw_score

    if board[i] != " ":
        return

    board[i] = current_player
    buttons[i].configure(
        text=current_player,
        text_color=COLOR_X if current_player == "X" else COLOR_O
    )

    if check_winner(current_player):
        if current_player == "X":
            x_score += 1
            winner = "Player X"
        else:
            o_score += 1
            winner = "Player O"

        update_score()
        messagebox.showinfo("Game Over", f"{winner} Wins!")
        reset_board()
        return

    if " " not in board:
        draw_score += 1
        update_score()
        messagebox.showinfo("Game Over", "Draw!")
        reset_board()
        return

    if game_mode == "FRIEND":
        current_player = "O" if current_player == "X" else "X"
    else:
        current_player = "O"
        move = ai_move()
        board[move] = "O"
        buttons[move].configure(text="O", text_color=COLOR_O)

        if check_winner("O"):
            o_score += 1
            update_score()
            messagebox.showinfo("Game Over", "AI Wins!")
            reset_board()
            return

        current_player = "X"

# ---------------- RESET ----------------
def reset_board():
    global board, current_player
    board = [" "] * 9
    current_player = "X"
    for btn in buttons:
        btn.configure(text="")

def reset_all():
    global x_score, o_score, draw_score
    x_score = o_score = draw_score = 0
    update_score()
    reset_board()

def change_mode(value):
    global game_mode
    game_mode = value
    reset_all()

# ---------------- UI ----------------
app = ctk.CTk()
app.title("Tic Tac Toe")
app.geometry("420x550")
app.resizable(False, False)

ctk.CTkLabel(
    app,
    text="TIC TAC TOE",
    font=("Segoe UI", 28, "bold")
).pack(pady=15)

score_label = ctk.CTkLabel(app, font=("Segoe UI", 15))
score_label.pack()
update_score()

mode_var = ctk.StringVar(value="FRIEND")
ctk.CTkOptionMenu(
    app,
    values=["FRIEND", "AI"],
    variable=mode_var,
    command=change_mode,
    width=200
).pack(pady=12)

board_frame = ctk.CTkFrame(app)
board_frame.pack(pady=20)

for i in range(9):
    btn = ctk.CTkButton(
        board_frame,
        text="",
        width=90,
        height=80,
        font=("Segoe UI", 28, "bold"),
        corner_radius=12,
        command=lambda i=i: on_click(i)
    )
    btn.grid(row=i//3, column=i%3, padx=10, pady=10)
    buttons.append(btn)

ctk.CTkButton(
    app,
    text="RESET GAME",
    fg_color="#ff5555",
    hover_color="#cc4444",
    font=("Segoe UI", 15, "bold"),
    command=reset_all,
    width=200
).pack(pady=20)

app.mainloop()
