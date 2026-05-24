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

def add_contact():
    try:
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        address = address_entry.get().strip()


        if not name or not phone or not address:
            messagebox.showwarning("Error", "Please fill all fields!")
            return


        contacts = load_contacts()
        contacts.append([name, phone, address])
        save_contacts(contacts)


        clear_fields()
        refresh_table()
        status_label.config(text="Added successfully.")


    except Exception as e:
        messagebox.showerror("Add Error", str(e))


def delete_contact():
    try:
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Warning", "Select a contact first!")
            return


        values = table.item(selected)["values"]
        if not values or values[1] == "No contact found":
            return


        index = int(values[0]) - 1
        contacts = load_contacts()


        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this contact?"
        )


        if not confirm:
            return


        if 0 <= index < len(contacts):
            contacts.pop(index)


        save_contacts(contacts)
        refresh_table()
        status_label.config(text="Deleted successfully.")


    except Exception as e:
        messagebox.showerror("Delete Error", str(e))
