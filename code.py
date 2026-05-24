import tkinter as tk
from tkinter import ttk, messagebox


FILE_NAME = "contacts.txt"


def load_contacts():
    contacts = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                data = line.strip().split("|")
                if len(data) == 3:
                    contacts.append(data)
    except FileNotFoundError:
        open(FILE_NAME, "w").close()
    except Exception as e:
        messagebox.showerror("Error", str(e))


    return contacts


def save_contacts(contacts):
    try:
        with open(FILE_NAME, "w") as file:
            for c in contacts:
                file.write("|".join(c) + "\n")
    except Exception as e:
        messagebox.showerror("Save Error", str(e))


def refresh_table(data=None):
    for row in table.get_children():
        table.delete(row)


    contacts = data if data is not None else load_contacts()


    if not contacts:
        table.insert("", "end", values=("", "No contact found", "", ""))
        return


    for i, c in enumerate(contacts, start=1):
        if i % 2 == 0:
            table.insert("", "end",
                         values=(i, c[0], c[1], c[2]),
                         tags=("evenrow",))
        else:
            table.insert("", "end",
                         values=(i, c[0], c[1], c[2]),
                         tags=("oddrow",))