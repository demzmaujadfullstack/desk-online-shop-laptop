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
