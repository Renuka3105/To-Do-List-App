# Tkinter To-Do List App with User Authentication

This is a desktop-based To-Do List application built using **Python and Tkinter**, enhanced with a **user login and registration system**. Each user has their own private task list, which is saved locally.



**FEATURES**

- **User Authentication**
  - Sign up / log in with username and password
  - Passwords are securely stored using SHA-256 hashing

- **Personal To-Do List**
  - Add, delete, and mark tasks as done
  - Data is saved per user using local `.pkl` files

- **Persistence**
  - Tasks and user data are saved even after restarting the app

- **Confirmation on Delete**
  - User is prompted before a task is removed

- **Clean, Dark-Themed UI**
  - Simple and visually friendly layout using Tkinter

  ## Project Structure
  ``` todo-tkinter-auth/
  ├── todo_app.py           # Main Python file (GUI, login, task logic) 
  ├── users.pkl             # Stores hashed usernames and passwords (auto-created)
  ├── tasks_<username>.pkl  # User-specific task files (created after login)
  ├── README.md             # Project documentation 
  └── __pycache__/          # Python cache files (auto-generated) 

