import tkinter as tk
from tkinter import messagebox
import random

# ---------- COLORS ----------
COLOR_X = "#1f4bd8"   # Blue
COLOR_O = "#d81f1f"   # Red

# ---------- GAME STATE ----------
board = [" "] * 9
buttons = []
current_player = "X"
game_mode = "FRIEND"  # AI or FRIEND

x_score = 0
o_score = 0
draw_score = 0

# ---------- GAME LOGIC ----------
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

# ---------- GAME FLOW ----------
def on_click(i):
    global current_player, x_score, o_score, draw_score

    if board[i] != " ":
        return

    if game_mode == "AI" and current_player != "X":
        return

    board[i] = current_player

    if current_player == "X":
        buttons[i].config(text="X", fg=COLOR_X)
    else:
        buttons[i].config(text="O", fg=COLOR_O)

    if check_winner(current_player):
        if current_player == "X":
            x_score += 1
            winner = "Player X"
        else:
            o_score += 1
            winner = "Player O"

        update_score()
        messagebox.showinfo("Game Over", f"{winner} wins!")
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
        buttons[move].config(text="O", fg=COLOR_O)

        if check_winner("O"):
            o_score += 1
            update_score()
            messagebox.showinfo("Game Over", "AI wins!")
            reset_board()
            return

        current_player = "X"

# ---------- RESET ----------
def reset_board():
    global board, current_player
    board = [" "] * 9
    current_player = "X"
    for btn in buttons:
        btn.config(text="", fg="black")

def reset_all():
    global x_score, o_score, draw_score
    x_score = o_score = draw_score = 0
    update_score()
    reset_board()

def update_score():
    score_label.config(
        text=f"X: {x_score}   O: {o_score}   Draws: {draw_score}"
    )

def change_mode(value):
    global game_mode
    game_mode = value
    reset_all()

# ---------- GUI ----------
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("360x500")
root.resizable(False, False)

tk.Label(root, text="Tic Tac Toe", font=("Arial", 22, "bold")).pack(pady=10)

score_label = tk.Label(root, font=("Arial", 12))
score_label.pack()
update_score()

mode_var = tk.StringVar(value="FRIEND")
tk.OptionMenu(root, mode_var, "FRIEND", "AI", command=change_mode).pack(pady=5)

board_frame = tk.Frame(root)
board_frame.pack(pady=15)

for i in range(9):
    btn = tk.Button(
        board_frame,
        text="",
        font=("Arial", 22, "bold"),
        width=5,
        height=2,
        command=lambda i=i: on_click(i)
    )
    btn.grid(row=i//3, column=i%3, padx=6, pady=6)
    buttons.append(btn)

tk.Button(root, text="Reset Game", command=reset_all).pack(pady=15)

root.mainloop()
