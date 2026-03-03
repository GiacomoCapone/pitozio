import tkinter as tk
from tkinter import messagebox

def aggiungi():
    testo = campo.get().strip()
    if testo:
        lista.insert(tk.END, testo)
        campo.delete(0, tk.END)
    else:
        messagebox.showwarning("Attenzione", "Scrivi qualcosa prima di aggiungere.")

def elimina():
    sel = lista.curselection()
    if sel:
        lista.delete(sel[0])

# Finestra
root = tk.Tk()
root.title("Inserimento & Visualizzazione")
root.geometry("500x350")

# Pannello SINISTRA
sx = tk.LabelFrame(root, text="Inserimento", padx=10, pady=10)
sx.pack(side="left", fill="both", expand=True, padx=10, pady=10)

tk.Label(sx, text="Testo:").pack(anchor="w")
campo = tk.Entry(sx, width=25)
campo.pack(pady=5)

tk.Button(sx, text="Aggiungi", command=aggiungi).pack(fill="x", pady=2)
tk.Button(sx, text="Elimina selezionato", command=elimina).pack(fill="x", pady=2)

# Pannello DESTRA
dx = tk.LabelFrame(root, text="Visualizzazione", padx=10, pady=10)
dx.pack(side="right", fill="both", expand=True, padx=10, pady=10)

lista = tk.Listbox(dx)
lista.pack(fill="both", expand=True)

root.mainloop()