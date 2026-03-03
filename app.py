import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2.extras import RealDictCursor

# ── Connessione ──────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "dbname":   "python",
    "user":     "postgres",
    "password": "$2005giac",
}

def get_conn():
    return psycopg2.connect(**DB_CONFIG)

# ── Carica dati nella tabella ────────────────
def carica():
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, code, description, ean_a, bought_at_price, price, department_id, storage_quantity FROM products ORDER BY id DESC")
        righe = cur.fetchall()
        cur.close()
        conn.close()

        tabella.delete(*tabella.get_children())
        for r in righe:
            tabella.insert("", "end", values=(
                r["id"], r["code"], r["description"], r["ean_a"],
                r["bought_at_price"], r["price"], r["department_id"], r["storage_quantity"]
            ))
    except Exception as e:
        messagebox.showerror("Errore DB", str(e))

# ── Inserisci record ─────────────────────────
def aggiungi():
    valori = {k: e.get().strip() for k, e in campi.items()}
    if not valori["code"]:
        messagebox.showwarning("Attenzione", "Il campo 'code' è obbligatorio.")
        return
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO products
                (code, description, alternative_description_a, alternative_description_b,
                 ean_a, ean_b, ean_c, bought_at_price, price, department_id, storage_quantity)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            valori["code"], valori["description"],
            valori["alt_desc_a"], valori["alt_desc_b"],
            valori["ean_a"], valori["ean_b"], valori["ean_c"],
            valori["bought_at_price"] or None,
            valori["price"] or None,
            valori["department_id"] or None,
            valori["storage_quantity"] or None,
        ))
        conn.commit()
        cur.close()
        conn.close()
        pulisci()
        carica()
        messagebox.showinfo("OK", "Prodotto inserito con successo.")
    except Exception as e:
        messagebox.showerror("Errore DB", str(e))

# ── Elimina record selezionato ───────────────
def elimina():
    sel = tabella.selection()
    if not sel:
        messagebox.showinfo("Info", "Seleziona un prodotto da eliminare.")
        return
    id_val = tabella.item(sel[0])["values"][0]
    if not messagebox.askyesno("Conferma", f"Eliminare il prodotto con id={id_val}?"):
        return
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id = %s", (id_val,))
        conn.commit()
        cur.close()
        conn.close()
        carica()
    except Exception as e:
        messagebox.showerror("Errore DB", str(e))

# ── Pulisci form ─────────────────────────────
def pulisci():
    for e in campi.values():
        e.delete(0, tk.END)

# ────────────────────────────────────────────
# UI
# ────────────────────────────────────────────
root = tk.Tk()
root.title("Gestione Prodotti")
root.geometry("1100x560")

# ── SINISTRA: form inserimento ───────────────
sx = tk.LabelFrame(root, text="Inserimento prodotto", padx=10, pady=10)
sx.pack(side="left", fill="y", padx=10, pady=10)

etichette = [
    ("Code *",              "code"),
    ("Description",         "description"),
    ("Alt. Description A",  "alt_desc_a"),
    ("Alt. Description B",  "alt_desc_b"),
    ("EAN A",               "ean_a"),
    ("EAN B",               "ean_b"),
    ("EAN C",               "ean_c"),
    ("Bought At Price",     "bought_at_price"),
    ("Price",               "price"),
    ("Department ID",       "department_id"),
    ("Storage Quantity",    "storage_quantity"),
]

campi = {}
for label, key in etichette:
    tk.Label(sx, text=label, anchor="w").pack(fill="x")
    entry = tk.Entry(sx, width=28)
    entry.pack(pady=(0, 4))
    campi[key] = entry

tk.Button(sx, text="Aggiungi", bg="#4ade80", command=aggiungi).pack(fill="x", pady=(8, 2))
tk.Button(sx, text="Pulisci", command=pulisci).pack(fill="x", pady=2)

# ── DESTRA: visualizzazione ──────────────────
dx = tk.LabelFrame(root, text="Prodotti nel database", padx=10, pady=10)
dx.pack(side="right", fill="both", expand=True, padx=10, pady=10)

cols = ("id", "code", "description", "ean_a", "bought_at_price", "price", "department_id", "storage_quantity")
tabella = ttk.Treeview(dx, columns=cols, show="headings", height=20)

for col in cols:
    tabella.heading(col, text=col)
    tabella.column(col, width=110, anchor="w")

scroll = ttk.Scrollbar(dx, orient="vertical", command=tabella.yview)
tabella.configure(yscrollcommand=scroll.set)
tabella.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

tk.Button(dx, text="🗑 Elimina selezionato", fg="red", command=elimina).pack(pady=(6, 0))
tk.Button(dx, text="↻ Aggiorna", command=carica).pack(pady=2)

# Carica dati all'avvio
carica()

root.mainloop()