
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
