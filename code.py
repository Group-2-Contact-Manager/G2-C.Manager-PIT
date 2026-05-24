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


def update_contact():
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


        if 0 <= index < len(contacts):
            contacts[index] = [
                name_entry.get(),
                phone_entry.get(),
                address_entry.get()
            ]


        save_contacts(contacts)
        refresh_table()
        clear_fields()


        status_label.config(text="Updated successfully.")


    except Exception as e:
        messagebox.showerror("Update Error", str(e))


def on_select(event):
    try:
        selected = table.focus()
        if not selected:
            return


        values = table.item(selected)["values"]


        if not values or values[1] == "No contact found":
            return


        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)


        name_entry.insert(0, values[1])
        phone_entry.insert(0, values[2])
        address_entry.insert(0, values[3])


    except Exception as e:
        messagebox.showerror("Select Error", str(e))


def search_contact(event=None):
    query = search_entry.get().lower()
    contacts = load_contacts()


    filtered = [
        c for c in contacts
        if query in c[0].lower() or query in c[1]
    ]


    refresh_table(filtered)


def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
