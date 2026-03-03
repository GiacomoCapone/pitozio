with open("input.txt", "r") as f:
    contenuto = f.read()
    f.close()
    righe = contenuto.splitlines()
    parole = contenuto.split()
print("numero totale di righe: {len(righe)}")
print("numero totale di parole: {len(parole)}")