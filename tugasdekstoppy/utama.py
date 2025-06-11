import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os
import sys
import subprocess
from PIL import Image, ImageTk

def connect_produk():
    return sqlite3.connect("produk.db")

def create_table_produk():
    conn = connect_produk()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            harga REAL,
            foto TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_data():
    for item in tree.get_children():
        tree.delete(item)

    conn = connect_produk()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert('', 'end', values=row)

def add_produk():
    nama = entry_nama.get()
    harga = entry_harga.get()
    foto = entry_foto.get()

    if not nama or not harga or not foto:
        messagebox.showwarning("Peringatan", "Semua field harus diisi.")
        return

    conn = connect_produk()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produk (nama, harga, foto) VALUES (?, ?, ?)", (nama, harga, foto))
    conn.commit()
    conn.close()

    load_data()
    clear_inputs()

def edit_produk():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Pilih Produk", "Pilih produk terlebih dahulu.")
        return

    values = tree.item(selected, 'values')
    id_produk = values[0]
    nama = entry_nama.get()
    harga = entry_harga.get()
    foto = entry_foto.get()

    if not nama or not harga or not foto:
        messagebox.showwarning("Peringatan", "Semua field harus diisi.")
        return

    conn = connect_produk()
    cursor = conn.cursor()
    cursor.execute("UPDATE produk SET nama=?, harga=?, foto=? WHERE id=?", (nama, harga, foto, id_produk))
    conn.commit()
    conn.close()

    load_data()
    clear_inputs()
    messagebox.showinfo("Sukses", "Data produk berhasil diubah.")

def hapus_produk():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Pilih Produk", "Pilih produk terlebih dahulu.")
        return

    values = tree.item(selected, 'values')
    id_produk = values[0]

    confirm = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus produk ini?")
    if not confirm:
        return

    conn = connect_produk()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produk WHERE id=?", (id_produk,))
    conn.commit()
    conn.close()

    load_data()
    clear_inputs()
    messagebox.showinfo("Sukses", "Produk berhasil dihapus.")

def clear_inputs():
    entry_nama.delete(0, tk.END)
    entry_harga.delete(0, tk.END)
    entry_foto.delete(0, tk.END)

def pilih_foto():
    file = filedialog.askopenfilename(filetypes=[("Gambar", "*.png *.jpg *.jpeg")])
    if file:
        entry_foto.delete(0, tk.END)
        entry_foto.insert(0, file)

def beli_produk():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Pilih Produk", "Pilih produk terlebih dahulu.")
        return

    values = tree.item(selected, 'values')
    id_produk, nama, harga, _ = values
    subprocess.Popen([sys.executable, "transaksi.py", str(nama), str(harga), str(user_name)])

def on_tree_select(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, 'values')
        entry_nama.delete(0, tk.END)
        entry_nama.insert(0, values[1])
        entry_harga.delete(0, tk.END)
        entry_harga.insert(0, values[2])
        entry_foto.delete(0, tk.END)
        entry_foto.insert(0, values[3])

# ====================== START GUI ========================
args = sys.argv
mode = args[1] if len(args) > 1 else "user"
user_name = args[2] if len(args) > 2 else "User"

root = tk.Tk()
root.title("Dashboard - TechLaptop")
root.geometry("1000x600")
root.configure(bg="#E3F2FD")

title = tk.Label(root, text=f"Selamat datang, {user_name}", font=("Arial", 16, "bold"), bg="#E3F2FD")
title.pack(pady=10)

# Form Admin
if mode == "admin":
    form_frame = tk.Frame(root, bg="#E3F2FD")
    form_frame.pack(pady=10)

    tk.Label(form_frame, text="Nama Laptop", bg="#E3F2FD").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_nama = tk.Entry(form_frame, width=40)
    entry_nama.grid(row=0, column=1, padx=5)

    tk.Label(form_frame, text="Harga", bg="#E3F2FD").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_harga = tk.Entry(form_frame, width=40)
    entry_harga.grid(row=1, column=1, padx=5)

    tk.Label(form_frame, text="Foto (path)", bg="#E3F2FD").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    entry_foto = tk.Entry(form_frame, width=40)
    entry_foto.grid(row=2, column=1, padx=5)
    tk.Button(form_frame, text="Browse", command=pilih_foto).grid(row=2, column=2)

    # Tombol CRUD
    button_frame = tk.Frame(root, bg="#E3F2FD")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Tambah Produk", command=add_produk, bg="#4CAF50", fg="white", width=18).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Ubah Produk", command=edit_produk, bg="#FFC107", fg="black", width=18).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Hapus Produk", command=hapus_produk, bg="#F44336", fg="white", width=18).pack(side=tk.LEFT, padx=10)

# Tabel Produk
tree = ttk.Treeview(root, columns=("ID", "Nama", "Harga", "Foto"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama Laptop")
tree.heading("Harga", text="Harga")
tree.heading("Foto", text="Path Gambar")
tree.pack(padx=20, pady=20, fill="both", expand=True)

tree.bind("<<TreeviewSelect>>", on_tree_select)

# Tombol beli untuk user
if mode != "admin":
    tk.Button(root, text="Beli Produk", command=beli_produk, bg="#1E88E5", fg="white").pack(pady=10)

create_table_produk()
load_data()
root.mainloop()
