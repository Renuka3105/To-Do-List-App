import tkinter as tk
from tkinter import messagebox
import pickle
import os
import hashlib

# File-based user and task storage
USER_FILE = "users.pkl"
TASK_FILE_PREFIX = "tasks_"

# --- User Authentication Functions ---
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "rb") as f:
            return pickle.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "wb") as f:
        pickle.dump(users, f)

# --- Login Window ---
def login_window():
    login_win = tk.Tk()
    login_win.title("Login or Register")
    login_win.geometry("300x200")

    tk.Label(login_win, text="Username").pack(pady=5)
    username_entry = tk.Entry(login_win)
    username_entry.pack()

    tk.Label(login_win, text="Password").pack(pady=5)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.pack()

    def attempt_login():
        username = username_entry.get()
        password = hash_password(password_entry.get())
        users = load_users()

        if username in users and users[username] == password:
            login_win.destroy()
            main_app(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def attempt_register():
        username = username_entry.get()
        password = hash_password(password_entry.get())
        users = load_users()

        if username in users:
            messagebox.showwarning("Warning", "Username already exists")
        else:
            users[username] = password
            save_users(users)
            messagebox.showinfo("Success", "Registration successful. You can now log in.")

    tk.Button(login_win, text="Login", command=attempt_login).pack(pady=5)
    tk.Button(login_win, text="Register", command=attempt_register).pack()
    login_win.mainloop()

# --- To-Do App Functions ---
def get_task_file(username):
    return f"{TASK_FILE_PREFIX}{username}.pkl"

def load_tasks(username):
    global task_list
    try:
        with open(get_task_file(username), "rb") as f:
            task_list = pickle.load(f)
            listbox.delete(0, tk.END)
            for task in task_list:
                listbox.insert(tk.END, task)
    except FileNotFoundError:
        task_list = []
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load tasks: {e}")

def save_tasks(username):
    try:
        with open(get_task_file(username), "wb") as f:
            pickle.dump(task_list, f)
        messagebox.showinfo("Success", "Tasks saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save tasks: {e}")

def add_task():
    task = task_entry.get().strip()
    if task:
        task_list.append(task)
        listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def remove_task():
    selected_item = listbox.curselection()
    if selected_item:
        index = selected_item[0]
        if index < len(task_list):
            confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this task?")
            if confirm:
                del task_list[index]
                listbox.delete(index)
    else:
        messagebox.showwarning("Warning", "Select a task to remove!")

def mark_done():
    selected_item = listbox.curselection()
    if selected_item:
        index = selected_item[0]
        if index < len(task_list):
            item = task_list[index]
            if item.startswith("✅"):
                task_list[index] = item[1:]
            else:
                task_list[index] = "✅" + item
            listbox.delete(index)
            listbox.insert(index, task_list[index])
    else:
        messagebox.showwarning("Warning", "Select a task to mark as done!")

# --- Main App ---
def main_app(username):
    global app, task_entry, listbox, task_list

    app = tk.Tk()
    app.title(f"{username}'s To-Do List")
    app.geometry("500x500")
    app.config(bg="#242424")

    task_list = []

    title = tk.Label(app, text="To-Do List", font=("Consolas", 18), bg="#242424", fg="#fff")
    title.pack(pady=10)

    task_entry = tk.Entry(app, width=40, font=("Consolas", 12))
    task_entry.pack(pady=10)

    button_frame = tk.Frame(app, bg="#242424")
    button_frame.pack()

    tk.Button(button_frame, text="Add", width=10, font=("Consolas", 12), command=add_task).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Remove", width=10, font=("Consolas", 12), command=remove_task).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="Mark Done", width=12, font=("Consolas", 12), command=mark_done).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(button_frame, text="Save", width=10, font=("Consolas", 12), command=lambda: save_tasks(username)).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(button_frame, text="Load", width=10, font=("Consolas", 12), command=lambda: load_tasks(username)).grid(row=1, column=2, padx=5, pady=5)

    listbox = tk.Listbox(app, height=15, width=50, font=("Consolas", 12))
    listbox.pack(pady=10)

    load_tasks(username)

    app.mainloop()

# --- Start App ---
login_window()