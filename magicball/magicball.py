import random
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

window = tk.Tk()
window.geometry("900x700")
window.title("Magic 8 Ball!")
window.configure(bg="#E4E9F7")

# -------------------- MAGIC 8 BALL FUNCTION --------------------
def ask_question():
    question = entry.get()
    if question.strip() == "":
        word_label.config(text="Please ask a question!")
        return

    num = random.randint(1, 9)
    answers = [
        "Yes - definitely",
        "It is decidedly so.",
        "Without a doubt.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful"
    ]
    word_label.config(text=answers[num-1])

# -------------------- WIDGETS --------------------
title = tk.Label(window, text="Magic 8 Ball", font=("Grand9K Pixel", 48), fg="#1B3366", bg="#E4E9F7")
title.pack(pady=20)

word_label = tk.Label(window, text="", font=("Grand9K Pixel", 32), fg="#46629E", bg="#E4E9F7")
word_label.pack(pady=30)

entry = tk.Entry(window, font=("Arial", 20), width=30)
entry.pack(pady=20)

guess_button = tk.Button(window, text="Enter Question", font=("Arial", 16), command=ask_question)
guess_button.pack(pady=10)

# -------------------- PIXELATED 8 BALL IMAGE --------------------
try:
    img = Image.open("magic.png")
    img = img.resize((400, 400), Image.NEAREST)  # Pixelated effect
    photo = ImageTk.PhotoImage(img)
    img_label = tk.Label(window, image=photo, bg="#E4E9F7")
    img_label.pack(pady=20)
except FileNotFoundError:
    img_label = tk.Label(window, text="Image not found!", font=("Arial", 16), bg="white")
    img_label.pack(pady=20)

# -------------------- ANIMATED GIF (KIRBY) --------------------
try:
    gif = Image.open("kirb.gif")
except FileNotFoundError:
    gif = None

gif_label = tk.Label(window, bg="#E4E9F7")
gif_label.lift()
gif_label.place(x=0, y=0)

# Keep frames in a global list
frames = []

if gif:
    for frame in ImageSequence.Iterator(gif):
        frame = frame.resize((1, 1), Image.NEAREST)
        frames.append(ImageTk.PhotoImage(frame))

    # Animation function
    def animate(index=0):
        frame = frames[index]
        gif_label.config(image=frame)
        gif_label.image = frame
        window.after(80, animate, (index + 1) % len(frames))


    print("GIF frames:", len(frames))
    animate()

##
gif2 = Image.open("spirit.gif")

gif2_label = tk.Label(window, bg="#E4E9F7")
gif2_label.place(x=0, y=4)

frames2 = []

for frame in ImageSequence.Iterator(gif2):
    frame = frame.copy()
    frame = frame.resize((200, 200), Image.NEAREST)
    frames2.append(ImageTk.PhotoImage(frame))


    def animate2(index=0):
        frame = frames2[index]
        gif2_label.config(image=frame)
        gif2_label.image = frame
        window.after(100, animate2, (index + 1) % len(frames2))


    print("GIF2 frames:", len(frames2))

    if len(frames2) > 1:
        animate2()

window.mainloop()
