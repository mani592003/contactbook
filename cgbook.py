import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

# File to save contacts
DATA_FILE = "contacts.json"

# Load contacts from file
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        contacts = json.load(f)
else:
    contacts = {}

# Save contacts to file
def save_contacts():
    with open(DATA_FILE, "w") as f:
        json.dump(contacts, f, indent=4)

# Add a new contact
def add_contact():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    email = email_entry.get().strip()
    address = address_entry.get().strip()

    if name == "" or phone == "":
        messagebox.showwarning("Input Error", "Name and phone are required.")
        return

    contacts[name] = {
        "phone": phone,
        "email": email,
        "address": address
    }

    save_contacts()
    messagebox.showinfo("Success", f"Contact '{name}' added.")
    clear_fields()
    view_contacts()

# Clear input fields
def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

# View all contacts
def view_contacts():
    listbox.delete(0, tk.END)
    for name, info in contacts.items():
        listbox.insert(tk.END, f"{name} - {info['phone']}")

# Search contact
def search_contact():
    query = search_entry.get().lower().strip()
    listbox.delete(0, tk.END)
    for name, info in contacts.items():
        if query in name.lower() or query in info["phone"]:
            listbox.insert(tk.END, f"{name} - {info['phone']}")

# Delete selected contact
def delete_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Contact", "Please select a contact to delete.")
        return

    contact_text = listbox.get(selected)
    name = contact_text.split(" - ")[0]

    if name in contacts:
        del contacts[name]
        save_contacts()
        messagebox.showinfo("Deleted", f"Contact '{name}' deleted.")
        view_contacts()

# Update selected contact
def update_contact():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Contact", "Please select a contact to update.")
        return

    contact_text = listbox.get(selected)
    name = contact_text.split(" - ")[0]

    if name in contacts:
        updated_phone = simpledialog.askstring("Update", "New phone:", initialvalue=contacts[name]["phone"])
        updated_email = simpledialog.askstring("Update", "New email:", initialvalue=contacts[name]["email"])
        updated_address = simpledialog.askstring("Update", "New address:", initialvalue=contacts[name]["address"])

        contacts[name] = {
            "phone": updated_phone or "",
            "email": updated_email or "",
            "address": updated_address or ""
        }

        save_contacts()
        messagebox.showinfo("Updated", f"Contact '{name}' updated.")
        view_contacts()

# GUI Setup
root = tk.Tk()
root.title("📒 Contact Book")
root.geometry("500x550")
root.configure(bg="#f0f0f0")

# Title
tk.Label(root, text="Contact Book", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=10)

# Form Inputs
tk.Label(root, text="Name:", bg="#f0f0f0").pack()
name_entry = tk.Entry(root, width=40)
name_entry.pack()

tk.Label(root, text="Phone:", bg="#f0f0f0").pack()
phone_entry = tk.Entry(root, width=40)
phone_entry.pack()

tk.Label(root, text="Email:", bg="#f0f0f0").pack()
email_entry = tk.Entry(root, width=40)
email_entry.pack()

tk.Label(root, text="Address:", bg="#f0f0f0").pack()
address_entry = tk.Entry(root, width=40)
address_entry.pack()

tk.Button(root, text="Add Contact", command=add_contact, bg="#4caf50", fg="white", width=20).pack(pady=5)

# Search Bar
tk.Label(root, text="Search by name or phone:", bg="#f0f0f0").pack()
search_entry = tk.Entry(root, width=30)
search_entry.pack()
tk.Button(root, text="Search", command=search_contact).pack(pady=5)

# Contact List
listbox = tk.Listbox(root, width=60, height=10)
listbox.pack(pady=10)

# Buttons
tk.Button(root, text="View All", command=view_contacts).pack()
tk.Button(root, text="Update", command=update_contact).pack(pady=5)
tk.Button(root, text="Delete", command=delete_contact, bg="#f44336", fg="white").pack(pady=5)

# Start GUI
view_contacts()  # Load contacts on startup
root.mainloop()
