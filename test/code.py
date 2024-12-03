import tkinter as tk
import customtkinter as ctk
from customtkinter import *
from persiantools.jdatetime import JalaliDate
import sqlite3
from tkinter import messagebox
import re
from kavenegar import *

# --- Constants ---
DB_FILE = 'pz.db'
API_KEY = "3936466A51684633482B34396E5541532F66585A455958385036674E54796A52694530396A48766E6574413D"
FONT = CTkFont(family="Vazir", size=25, weight='bold')
FONT_ENTRY = CTkFont(family="Vazir", size=20)
DARK_MODE = "dark"

# --- Database Functions ---
def create_db():
    conn = sqlite3.connect(DB_FILE)
    conn.execute('''CREATE TABLE IF NOT EXISTS paziresh (
                        id INTEGER PRIMARY KEY,
                        arrival TEXT NOT NULL,
                        departure TEXT,
                        system TEXT NOT NULL,
                        system_type TEXT NOT NULL,
                        system_model TEXT NOT NULL,
                        system_serial INTEGER NOT NULL,
                        input_name TEXT NOT NULL,
                        tel TEXT NOT NULL,
                        code_meli TEXT NOT NULL,
                        tel_sabet TEXT,
                        adress TEXT NOT NULL,
                        problem TEXT NOT NULL,
                        cost REAL,
                        description TEXT NOT NULL,
                        Warranty TEXT NOT NULL
                    )''')
    conn.commit()
    conn.close()

def db_insert(data):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO paziresh VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def db_query(query): #Helper for querying database
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

# --- Validation Functions ---
def validate_phone(phone):
    return bool(re.match(r"^\+?\d{10,15}$", phone))

def validate_code_meli(code):
    return bool(re.match(r"^\d{10}$", code))


# --- UI Functions ---
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def close_window():
    root.destroy()


def show_dashboard():
    clear_frame(root) #Clear main root frame
    dashboard_frame = CTkFrame(root)
    dashboard_frame.grid(row=1, column=0, rowspan=7, sticky=NSEW)
    dashboard_frame.grid_columnconfigure(0, weight=1)
    dashboard_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
    
    create_buttons(dashboard_frame, [
        ("پذیرش", show_paziresh),
        ("ارسال پیامک", show_sms),
        ("تاریخچه", show_tarikh),
        ("خروج", close_window, "#EA0000", "#B20000") #Custom color for exit button
    ])


def create_buttons(parent, button_data):
    for i, (text, command, fg_color="#009933", hover_color="#00ff00") in enumerate(button_data):
        button = CTkButton(parent, text=text, font=FONT, fg_color=fg_color, hover_color=hover_color, command=command)
        button.grid(row=i + 1, column=0, padx=20, pady=20)


# --- Paziresh (Reception) UI ---
def show_paziresh():
    create_db()
    clear_frame(root)
    
    # Get next ID
    next_id = db_query("SELECT MAX(id) FROM paziresh")[0][0] + 1 if db_query("SELECT MAX(id) FROM paziresh")[0][0] is not None else 1
    next_id += 1590
    
    def save_paziresh_data():
        try:
            data = [
                ent_date_of_arrival.get(),
                ent_departure_date.get(),
                ent_input_system.get(),
                combo_input_system_type.get(),
                ent_input_system_model.get(),
                int(ent_input_system_serial.get()),
                ent_input_name.get(),
                ent_input_name_tel.get(),
                ent_input_name_code_meli.get(),
                ent_input_name_tel_sabet.get(),
                ent_input_name_adress.get("1.0", tk.END).strip(),
                ent_problem.get(),
                float(ent_cost.get()),
                ent_input_description.get("1.0", tk.END).strip(),
                chek.get()
            ]

            if not all(data[2:8]): #Validate Required fields
                return messagebox.showerror("Error", "Please fill in all required fields.")
            
            if not validate_phone(data[7]):
                return messagebox.showerror("Error", "Invalid phone number.")
            if not validate_code_meli(data[8]):
                return messagebox.showerror("Error", "Invalid code meli.")
            
            data.insert(0, next_id) #Add ID at the beginning
            if db_insert(tuple(data)):
                messagebox.showinfo("Success", "Data saved successfully!")
            else:
                messagebox.showerror("Error", "Database error") #Simpler error message
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            
        show_dashboard()

    # ... (Rest of the paziresh_ UI code remains largely the same, but  use create_entry_label_pair function below)
    paziresh_frame = CTkFrame(root)
    paziresh_frame.grid(row=1, column=0, rowspan=7, sticky=NSEW)
    create_entry_label_pair(paziresh_frame, "شماره پذریش", next_id, state=DISABLED, row=0, col=4)
    create_entry_label_pair(paziresh_frame, "تاریخ ورود", JalaliDate.today().strftime('%Y/%m/%d'), state=DISABLED, row=0, col=2)
    create_entry_label_pair(paziresh_frame, "تاریخ خروج", "", row=0, col=0) #Departure Date
    # ... and the rest of the paziresh fields using the new function


# Helper function to reduce redundancy in creating label-entry pairs
def create_entry_label_pair(parent, label_text, entry_value="", state=NORMAL, row=0, col=0, justify='right'):
    lbl = CTkLabel(parent, text=f":{label_text}", font=FONT)
    lbl.grid(row=row, column=col + 1, pady=5)
    ent = CTkEntry(parent, font=FONT_ENTRY, justify=justify, state=state)
    ent.grid(row=row, column=col, pady=5)
    ent.insert(0, entry_value)
    return ent


# ... (SMS and Tarikh (History) functions with similar optimizations for less redundancy)

# --- Main ---
ctk.set_appearance_mode(DARK_MODE)
ctk.set_default_color_theme("dark-blue")

root = CTk()
root.iconbitmap('tv.ico')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure((0, 1, 2, 3), weight=0)
root.grid_rowconfigure((4, 5, 6, 7), weight=1)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

api = KavenegarAPI(API_KEY)

show_dashboard() #Start with dashboard
root.mainloop()
