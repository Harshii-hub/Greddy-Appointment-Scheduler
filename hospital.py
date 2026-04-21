import tkinter as tk
from tkinter import messagebox
import sqlite3

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient TEXT,
    start INTEGER,
    end INTEGER
)
""")
conn.commit()

# ---------------- LOGIN FUNCTION ----------------
def login():
    if username.get() == "admin" and password.get() == "1234":
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# ---------------- MAIN WINDOW ----------------
def open_main_window():
    root = tk.Tk()
    root.title("Hospital Appointment System")
    root.geometry("650x550")

    tk.Label(root, text="Hospital Appointment Scheduler",
             font=("Arial", 16, "bold")).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=10)

    tk.Label(frame, text="Patient Name").grid(row=0, column=0)
    patient_entry = tk.Entry(frame)
    patient_entry.grid(row=0, column=1)

    tk.Label(frame, text="Start Time").grid(row=1, column=0)
    start_entry = tk.Entry(frame)
    start_entry.grid(row=1, column=1)

    tk.Label(frame, text="End Time").grid(row=2, column=0)
    end_entry = tk.Entry(frame)
    end_entry.grid(row=2, column=1)

    # -------- LISTBOX --------
    listbox = tk.Listbox(root, width=60)
    listbox.pack(pady=10)

    # -------- ADD APPOINTMENT --------
    def add_appointment():
        try:
            p = patient_entry.get()
            s = int(start_entry.get())
            e = int(end_entry.get())

            if p == "":
                messagebox.showerror("Error", "Enter patient name")
                return

            if s >= e:
                messagebox.showerror("Error", "Start time must be less than End time")
                return

            cursor.execute(
                "INSERT INTO appointments (patient, start, end) VALUES (?, ?, ?)",
                (p, s, e)
            )
            conn.commit()

            listbox.insert(tk.END, f"{p} | {s} - {e}")

            patient_entry.delete(0, tk.END)
            start_entry.delete(0, tk.END)
            end_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers for time")

    tk.Button(root, text="Add Appointment",
              command=add_appointment, bg="lightblue").pack(pady=5)

    # -------- LOAD DATA --------
    def load_data():
        listbox.delete(0, tk.END)
        cursor.execute("SELECT * FROM appointments")
        rows = cursor.fetchall()

        for row in rows:
            listbox.insert(tk.END, f"{row[1]} | {row[2]} - {row[3]}")

    tk.Button(root, text="Load Appointments",
              command=load_data).pack(pady=5)

    # -------- GREEDY SCHEDULER --------
    def run_scheduler():
        cursor.execute("SELECT patient, start, end FROM appointments")
        data = cursor.fetchall()

        if not data:
            messagebox.showwarning("Warning", "No appointments available")
            return

        data.sort(key=lambda x: x[2])  # sort by end time

        selected = [data[0]]
        last_end = data[0][2]

        for i in range(1, len(data)):
            if data[i][1] >= last_end:
                selected.append(data[i])
                last_end = data[i][2]

        result_box.delete("1.0", tk.END)
        result_box.insert(tk.END, "Optimized Schedule:\n\n")

        for p, s, e in selected:
            result_box.insert(tk.END, f"{p} | {s} - {e}\n")

    tk.Button(root, text="Run Greedy Scheduler",
              command=run_scheduler, bg="lightgreen").pack(pady=5)

    # -------- RESULT BOX --------
    result_box = tk.Text(root, height=10, width=60)
    result_box.pack(pady=10)

    root.mainloop()

# ---------------- LOGIN WINDOW ----------------
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x220")

tk.Label(login_window, text="Admin Login",
         font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(login_window, text="Username").pack()
username = tk.Entry(login_window)
username.pack()

tk.Label(login_window, text="Password").pack()
password = tk.Entry(login_window, show="*")
password.pack()

tk.Button(login_window, text="Login",
          command=login, bg="lightblue").pack(pady=10)

login_window.mainloop()