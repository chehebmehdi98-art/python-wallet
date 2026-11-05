import tkinter as tk
from tkinter import messagebox
import csv
import os
from datetime import datetime


solde = 0
operations = []
types = set()

total_depot = 0
total_retrait = 0


def lire_csv():
    global solde, total_depot, total_retrait

    if os.path.exists("wallet.csv"):
        with open("wallet.csv", "r") as f:
            reader = csv.reader(f)

            for ligne in reader:
                if len(ligne) < 3:
                    continue

                type_op = ligne[0]
                montant = int(ligne[1])
                date = ligne[2]

                op = {"type": type_op, "montant": montant, "date": date}

                operations.append(op)
                types.add(type_op)

                if type_op == "depot":
                    solde += montant
                    total_depot += montant
                else:
                    solde -= montant
                    total_retrait += montant


def save_csv(type_op, montant, date):
    with open("wallet.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([type_op, montant, date])


def ajouter():
    global solde, total_depot

    try:
        montant = int(champ.get())

        if montant <= 0:
            messagebox.showwarning("Attention", "Montant invalide")
            return

        date = datetime.now().strftime("%d/%m/%Y %H:%M")

        solde += montant
        total_depot += montant

        op = {"type": "depot", "montant": montant, "date": date}
        operations.append(op)
        types.add("depot")

        save_csv("depot", montant, date)

        update_all()
        champ.delete(0, tk.END)

    except:
        messagebox.showerror("Erreur", "Entrer un nombre valide")


def retirer():
    global solde, total_retrait

    try:
        montant = int(champ.get())

        if montant <= 0:
            messagebox.showwarning("Attention", "Montant invalide")
            return

        if montant <= solde:
            date = datetime.now().strftime("%d/%m/%Y %H:%M")

            solde -= montant
            total_retrait += montant

            op = {"type": "retrait", "montant": montant, "date": date}
            operations.append(op)
            types.add("retrait")

            save_csv("retrait", montant, date)

            update_all()
            champ.delete(0, tk.END)

        else:
            messagebox.showwarning("Attention", "Solde insuffisant")

    except:
        messagebox.showerror("Erreur", "Entrer un nombre valide")


def update_all():
    label_solde.config(text="Solde : " + str(solde) + " DH")
    label_stats.config(text=f"Depot: {total_depot} DH | Retrait: {total_retrait} DH")


def afficher_ops():
    zone.delete("1.0", tk.END)

    for op in operations:
        texte = f"{op['type']} : {op['montant']} DH | {op['date']}"
        zone.insert(tk.END, texte + "\n")


fenetre = tk.Tk()
fenetre.title("Wallet App")
fenetre.geometry("350x450")
fenetre.configure(bg="#c8c8c8")

champ = tk.Entry(fenetre, font=("Arial", 14))
champ.pack(pady=10)

tk.Button(fenetre, text="Ajouter", bg="green", fg="white", width=15, command=ajouter).pack(pady=5)
tk.Button(fenetre, text="Retirer", bg="red", fg="white", width=15, command=retirer).pack(pady=5)
tk.Button(fenetre, text="Afficher Operations", bg="blue", fg="white", width=20, command=afficher_ops).pack(pady=5)

label_solde = tk.Label(fenetre, text="Solde : 0 DH", fg="white", bg="#121010", font=("Arial", 14))
label_solde.pack(pady=10)

label_stats = tk.Label(fenetre, text="Depot: 0 | Retrait: 0", fg="white", bg="#000000")
label_stats.pack()

zone = tk.Text(fenetre, height=10, width=40)
zone.pack(pady=10)

lire_csv()
update_all()

fenetre.mainloop()
