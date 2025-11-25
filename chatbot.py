import tkinter as tk
from tkinter import scrolledtext
from tkinter import Canvas, PhotoImage
import json
import random
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import pyttsx3
from PIL import Image, ImageTk, ImageDraw

# ------------------- VOSK & TTS -------------------
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen_voice():
    chat_area.insert(tk.END, "\n🎙 Listening...\n", "bot")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16", channels=1) as stream:
        while True:
            data, _ = stream.read(4000)
            data_bytes = bytes(data)  # <-- convert to bytes for Vosk
            if recognizer.AcceptWaveform(data_bytes):
                result = json.loads(recognizer.Result())
                return result.get("text", "").lower()


# ------------------- THEMES -------------------
themes = {
    "dark": {"bg":"#0A0F24","chat_bg":"#11182F","user_color":"#FF6B9A","bot_color":"#AAAAAA","text":"white","star":"white"},
    "light":{"bg":"#FFFFFF","chat_bg":"#ECECEC","user_color":"#FF6B9A","bot_color":"#AAAAAA","text":"black","star":"gold"},
    "blue":{"bg":"#002B55","chat_bg":"#003C7A","user_color":"#FF6B9A","bot_color":"#AAAAAA","text":"white","star":"white"}
}
current_theme = "dark"

# ------------------- CHATBOT LOGIC -------------------
def bot_response(user_text):
    user = user_text.lower()
    if any(x in user for x in ["hello", "hi"]):
        return "Hello! How can I help you?"
    elif "name" in user:
        return "I am your NiaBot !"
    elif "developed" in user or "who made you" in user:
        return "I was developed by Niharikaa Singh."
    
    elif "python" in user:
        return "Python is a beginner-friendly programming language!"
    elif "java" in user:
        return "Java is a versatile language, widely used for enterprise applications."

    elif "machine learning" in user:
        return "Machine learning is teaching computers to learn from data."

    elif "AI" in user or "artificial intelligence" in user:
        return "AI is the simulation of human intelligence by machines."
    elif "joke" in user:
        return "Why do programmers prefer dark mode? Because light attracts bugs!"

    elif "how are you" in user:
        return "I'm doing great, thank you! How about you?"

    elif "weather" in user:
        return "I can't check live weather yet, but it's always sunny in the digital world."

    elif "favorite color" in user:
        return "I like all colors! But right now, I am feeling blue."
    elif "voice recognition" in user:
        return "Yes! I can understand and answer if you speak something to me."

    elif any(x in user for x in ["exit","bye"]):
        return "Have a great day byeee!!!."
        root.destroy()
    else:
        return "Sorry, I didn’t understand that."

# ------------------- GUI -------------------
root = tk.Tk()
root.title("Voice Chatbot")
root.geometry("800x700")
root.configure(bg=themes[current_theme]["bg"])
root.resizable(True, True)

# Canvas for background + stars
canvas = Canvas(root, width=800, height=700, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Chat frame (glass effect)
chat_frame = tk.Frame(canvas, bg="#11182F", bd=0)
chat_frame.place(x=220, y=50, width=550, height=580)

# Chat area
chat_area = tk.Text(chat_frame, wrap=tk.WORD, font=("Segoe UI", 12), bg="#11182F", bd=0, padx=10, pady=10)
chat_area.pack(fill=tk.BOTH, expand=True)

# Entry + buttons
entry_box = tk.Entry(chat_frame, font=("Segoe UI", 13))
entry_box.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

def insert_message(message, sender):
    """Create rounded chat bubble for messages."""
    chat_area.configure(state="normal")
    if sender=="user":
        chat_area.insert(tk.END, f"\n")
        chat_area.window_create(tk.END, window=create_bubble(message, "user"))
        chat_area.insert(tk.END, "\n")
    else:
        chat_area.insert(tk.END, f"\n")
        chat_area.window_create(tk.END, window=create_bubble(message, "bot"))
        chat_area.insert(tk.END, "\n")
    chat_area.see(tk.END)
    chat_area.configure(state="disabled")

def create_bubble(text, sender):
    """Return a frame with rounded background for a message."""
    frame = tk.Frame(chat_area, bg=themes[current_theme]["chat_bg"])
    color = themes[current_theme]["user_color"] if sender=="user" else themes[current_theme]["bot_color"]
    bubble = tk.Label(frame, text=text, bg=color, fg="white", font=("Segoe UI", 12), padx=10, pady=5, wraplength=350, justify="left")
    bubble.pack(side=tk.RIGHT if sender=="user" else tk.LEFT, anchor="e" if sender=="user" else "w")
    bubble.configure(relief="ridge", bd=5)
    bubble.configure(highlightthickness=0)
    return frame

# Buttons
def send_message():
    user_text = entry_box.get()
    if not user_text: return
    insert_message(user_text, "user")
    entry_box.delete(0, tk.END)
    reply = bot_response(user_text)
    insert_message(reply, "bot")
    speak(reply)

send_btn = tk.Button(chat_frame, text="Send", font=("Segoe UI", 11), command=send_message)
send_btn.pack(side=tk.LEFT, padx=5)

def voice_message():
    text = listen_voice()
    insert_message(text, "user")
    reply = bot_response(text)
    insert_message(reply, "bot")
    speak(reply)

mic_btn = tk.Button(chat_frame, text="🎤", font=("Segoe UI", 12), width=4, command=voice_message)
mic_btn.pack(side=tk.LEFT, padx=5)

def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme=="dark" else "blue" if current_theme=="light" else "dark"
    apply_theme()

toggle_btn = tk.Button(chat_frame, text="Theme", font=("Segoe UI", 11), command=toggle_theme)
toggle_btn.pack(side=tk.LEFT, padx=5)

# ------------------- Avatar -------------------
def create_circle_avatar(img_path, size=(100,100)):
    img = Image.open(img_path).resize(size, Image.Resampling.LANCZOS)
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0,0,size[0],size[1]), fill=255)
    img.putalpha(mask)
    return ImageTk.PhotoImage(img)

avatar_img = create_circle_avatar("chatbot.png", size=(120,120))
avatar_label = tk.Label(canvas, image=avatar_img, bg=themes[current_theme]["bg"])
avatar_label.place(x=50, y=50)

# ------------------- Star Background -------------------
stars = []
for _ in range(150):
    x, y = random.randint(0, 800), random.randint(0,700)
    star = canvas.create_oval(x, y, x+2, y+2, fill=themes[current_theme]["star"], outline="")
    stars.append(star)

def update_stars():
    for star in stars:
        canvas.itemconfig(star, fill=themes[current_theme]["star"])
    root.after(500, update_stars)

# ------------------- Apply Theme -------------------
def apply_theme():
    theme = themes[current_theme]
    root.configure(bg=theme["bg"])
    canvas.configure(bg=theme["bg"])
    chat_frame.configure(bg=theme["chat_bg"])
    chat_area.configure(bg=theme["chat_bg"], fg=theme["text"])
    entry_box.configure(bg=theme["chat_bg"], fg=theme["text"], insertbackground=theme["text"])
    send_btn.configure(bg=theme["user_color"], fg="black")
    mic_btn.configure(bg=theme["bot_color"], fg="black")
    toggle_btn.configure(bg=theme["bot_color"], fg="black")
    avatar_label.configure(bg=theme["bg"])
    update_stars()

apply_theme()
root.mainloop()
