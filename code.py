import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "contacts.txt"

def load_contacts():
    contacts = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                data = line.strip().split(" | ")
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
                file.write(" | ".join(c) + "\n")
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
            table.insert("", "end", values=(i, c[0], c[1], c[2]), tags=("even row",))
        else:
            table.insert("", "end", values=(i, c[0], c[1], c[2]), tags=("odd row",))

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

        confirm = messagebox.askyesno("Confirm Delete", "Do you want to delete this contact?")

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
            contacts[index] = [name_entry.get(), phone_entry.get(), address_entry.get()]

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

        for entry in (name_entry, phone_entry, address_entry):
            entry.delete(0, tk.END)

        name_entry.insert(0, values[1])
        phone_entry.insert(0, values[2])
        address_entry.insert(0, values[3])

    except Exception as e:
        messagebox.showerror("Select Error", str(e))

def search_contact(event=None):
    query = search_entry.get().lower()
    contacts = load_contacts()

    filtered = [c for c in contacts if query in c[0].lower() or query in c[1].lower()]

    refresh_table(filtered)

def clear_fields():
    for entry in (name_entry, phone_entry, address_entry):
        entry.delete(0, tk.END)

def call_contact():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact first!")
        return

    values = table.item(selected)["values"]
    phone = values[2]

    messagebox.showinfo("Call", f"Calling {phone}...")


def message_contact():
    selected = table.focus()
    if not selected:
        messagebox.showwarning("Warning", "Select a contact first!")
        return

    values = table.item(selected)["values"]
    phone = values[2]

    messagebox.showinfo("Message", f"Messaging {phone}...")

root = tk.Tk()
root.title("CONTACT MANAGER")
root.geometry("1050x650")
root.configure(bg="#83004f")

left = tk.Frame(root, bg="#83004f", width=300)
left.pack(side="left", fill="y")

tk.Label(left, text="CONTACT MANAGER", bg="#83004f", fg="white", font=("Segoe UI", 20, "bold")).pack(pady=15, padx=15)

tk.Label(left, text="FULL NAME", bg="#83004f", fg="#ffffff").pack(anchor="w", padx=20)
name_entry = tk.Entry(left, bg="#fcbce2", fg="black", insertbackground="black", font=("Segoe UI", 11), width=28)
name_entry.pack(padx=20, pady=4, fill="x", ipady=3)

tk.Label(left, text="PHONE NUMBER", bg="#83004f", fg="#ffffff").pack(anchor="w", padx=20)
phone_entry = tk.Entry(left, bg="#fcbce2", fg="black", insertbackground="black", font=("Segoe UI", 11), width=28)
phone_entry.pack(padx=20, pady=4, fill="x", ipady=3)

tk.Label(left, text="ADDRESS", bg="#83004f", fg="#ffffff").pack(anchor="w", padx=20)
address_entry = tk.Entry(left, bg="#fcbce2", fg="black", insertbackground="black", font=("Segoe UI", 11), width=28)
address_entry.pack(padx=20, pady=4, fill="x", ipady=3)

btn_font = ("Segoe UI", 11)

tk.Button(left, text="Add Contact", bg="#3d6fc1", fg="white", font=btn_font, command=add_contact).pack(padx=20, pady=10, fill="x", ipady=2)

tk.Button(left, text="Update Contact", bg="#8b5cf6", fg="white", font=btn_font, command=update_contact).pack(padx=20, pady=10, fill="x", ipady=2)

tk.Button(left, text="Delete Contact", bg="#ef4444", fg="white", font=btn_font, command=delete_contact).pack(padx=20, pady=10, fill="x", ipady=2)

tk.Button(left, text="Clear Fields", bg="#8f887e", fg="white", font=btn_font, command=clear_fields).pack(padx=20, pady=10, fill="x", ipady=2)

tk.Button(left, text="Call Contact", bg="#22c55e", fg="white", font=btn_font, command=call_contact).pack(padx=75, pady=5, fill="x", ipady=5)

tk.Button(left, text="Message Contact", bg="#06b6d4", fg="white", font=btn_font, command=message_contact).pack(padx=75, pady=5, fill="x", ipady=5)

right = tk.Frame(root, bg="#83004f")
right.pack(side="right", expand=True, fill="both")

header = tk.Frame(right, bg="#83004f")
header.pack(fill="x", padx=15, pady=8)

tk.Label(header, text="ALL CONTACTS", bg="#83004f", fg="white", font=("Segoe UI", 11, "bold")).pack(side="left", padx=10)

search_frame = tk.Frame(header, bg="#83004f")
search_frame.pack(side="right", padx=5)

search_label = tk.Label(search_frame, text="🔍", bg="#83004f", fg="#d1d5db", font=("Segoe UI", 11))
search_label.pack(side="left", padx=(8, 4))

search_text = tk.Label(search_frame, text="Search...", bg="#83004f", fg="#d1d5db", font=("Segoe UI", 11))
search_text.pack(side="left", padx=(5, 8), pady=4, ipady=2)

search_entry = tk.Entry(search_frame, width=25, font=("Segoe UI", 11))
search_entry.pack(side="left", ipady=3)
search_entry.bind("<KeyRelease>", search_contact)

status_label = tk.Label(right, text="", bg="#83004f", fg="#48ffbc", font=("Segoe UI", 9))
status_label.pack(side="bottom", anchor="w", pady=3, padx=12, ipady=2)

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview", background="#fcbce2", foreground="black", fieldbackground="#83004f")

style.configure("Treeview.Heading", background="#83004f", foreground="white")

columns = ("#", "Name", "Phone Number", "Address")

table = ttk.Treeview(right, columns=columns, show="headings", height=25)

for col in columns:
    table.heading(col, text=col)

table.column("#", width=50, anchor="center")
table.column("Name", width=200)
table.column("Phone Number", width=170)
table.column("Address", width=260)

style.configure("Treeview", rowheight=28)

table.pack(padx=15, pady=8, fill="both", expand=True)

table.bind("<<TreeviewSelect>>", on_select)

refresh_table()

root.mainloop()
