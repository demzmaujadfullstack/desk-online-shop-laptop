import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os

def connect_db():
    return sqlite3.connect("users.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            email TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def register_user():
    nama = entry_nama.get()
    email = entry_email.get()
    password = entry_password.get()

    if not email.endswith('@gmail.com'):
        messagebox.showwarning("Email Error", "Email harus berakhiran @gmail.com!")
        return

    if nama and email and password:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (nama, email, password) VALUES (?, ?, ?)", (nama, email, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Registration Success", "Pendaftaran berhasil!")
        root.destroy()
        subprocess.Popen(['python', 'login.py'], cwd=os.path.dirname(__file__))
    else:
        messagebox.showwarning("Input Error", "Semua field harus diisi!")

def back_to_pembuka():
    root.destroy()
    subprocess.Popen(['python', 'pembuka.py'], cwd=os.path.dirname(__file__))

root = tk.Tk()
root.title("Pendaftaran Pengguna")
root.geometry("800x600")
root.configure(bg='#87CEFA')

input_frame = tk.Frame(root, bg='#87CEFA')
input_frame.pack(pady=50)

label_nama = tk.Label(input_frame, text="Nama", font=("Arial", 12), bg='#87CEFA')
label_nama.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_nama = tk.Entry(input_frame, font=("Arial", 14), width=30)
entry_nama.grid(row=0, column=1, padx=10, pady=10)

label_email = tk.Label(input_frame, text="Email", font=("Arial", 12), bg='#87CEFA')
label_email.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_email = tk.Entry(input_frame, font=("Arial", 14), width=30)
entry_email.grid(row=1, column=1, padx=10, pady=10)

label_password = tk.Label(input_frame, text="Password", font=("Arial", 12), bg='#87CEFA')
label_password.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_password = tk.Entry(input_frame, font=("Arial", 14), show="*", width=30)
entry_password.grid(row=2, column=1, padx=10, pady=10)

btn_register = tk.Button(root, text="Daftar", command=register_user, font=("Arial", 14), width=20, bg='#4CAF50', fg='white')
btn_register.pack(pady=20)

btn_back = tk.Button(root, text="Back", command=back_to_pembuka, font=("Arial", 14), width=20, bg='red', fg='white')
btn_back.pack(pady=5)

create_table()
root.mainloop()
