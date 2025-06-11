import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

def open_login():
    try:
        root.destroy()
        subprocess.Popen(["python", "login.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

def open_register():
    try:
        root.destroy()
        subprocess.Popen(["python", "register.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

root = tk.Tk()
root.title("TechLaptop - Selamat Datang")
root.geometry("800x600")
root.configure(bg="#1E88E5")

# Logo (jika tersedia)
logo_frame = tk.Frame(root, bg="#1E88E5")
logo_frame.pack(expand=True)

try:
    img = Image.open("logo.jpg")
    img = img.resize((450, 300), Image.LANCZOS)
    logo = ImageTk.PhotoImage(img)
    label = tk.Label(logo_frame, image=logo, bg="#1E88E5")
    label.image = logo
    label.pack()
except:
    label = tk.Label(logo_frame, text="TechLaptop", font=("Arial", 28, "bold"), bg="#1E88E5", fg="white")
    label.pack()

# Tombol
btn_frame = tk.Frame(root, bg="#1E88E5")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Login", command=open_login, font=("Arial", 14), width=15, bg="#43A047", fg="white").pack(side="left", padx=10)
tk.Button(btn_frame, text="Register", command=open_register, font=("Arial", 14), width=15, bg="#FB8C00", fg="white").pack(side="left", padx=10)

root.mainloop()
