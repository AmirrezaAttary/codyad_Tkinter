import tkinter as tk
import customtkinter
from customtkinter import *
from persiantools.jdatetime import JalaliDate
import sqlite3
from tkinter import messagebox
import re #for regex validation

DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("dark-blue")

def create_database():
  conn = sqlite3.connect('pz.db')
  cursor = conn.cursor()
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS paziresh (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      arrival TEXT,
      departure TEXT,
      system TEXT,
      system_type TEXT,
      system_model TEXT,
      system_serial INTEGER,
      input_name TEXT,
      tel TEXT,
      code_meli TEXT,
      tel_sabet TEXT,
      adress TEXT,
      problem TEXT,
      cost REAL,
      description TEXT
    )
  ''')
  conn.commit()
  conn.close()

def validate_phone(phone_number):
  #Basic phone number validation (adjust regex as needed)
  pattern = r"^\+?\d{10,15}$" #Example: Accepts numbers starting with optional +, min 10 digits
  return bool(re.match(pattern, phone_number))

def validate_code_meli(code_meli):
  #Basic code meli validation (Adjust if needed)
  pattern = r"^\d{10}$" # Example: 10 digits
  return bool(re.match(pattern, code_meli))

def insert_data(data):
  try:
    conn = sqlite3.connect('pz.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO paziresh (arrival, departure, system, system_type, system_model, system_serial, input_name, tel, code_meli, tel_sabet, adress, problem, cost, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    return True # Success
  except sqlite3.IntegrityError:
    return "Duplicate entry, please review the inputs."
  except sqlite3.Error as e:
    return f"Database error: {e}"
  finally:
    conn.close()

def clear_frame(frame):
  for widget in frame.winfo_children():
    widget.destroy()

def close_window():
  root.destroy()

# ... [rest of your functions remain largely the same, but incorporate the changes below]

def paziresh_():
  clear_frame(far)
  # ... (Your existing code for paziresh_)

  def save_data():
    try:
      arrival = ent_date_of_arrival.get()
      departure = ent_departure_date.get()
      # ... get other data fields ...
      system = ent_input_system.get()
      system_type = combo_input_system_type.get()
      system_model = ent_input_system_model.get()
      try:
        system_serial = int(ent_input_system_serial.get())
      except ValueError:
        return messagebox.showerror("Error", "Serial number must be an integer.")
      input_name = ent_input_name.get()
      tel = ent_input_name_tel.get()
      code_meli = ent_input_name_code_meli.get()
      tel_sabet = ent_input_name_tel_sabet.get()
      adress = ent_input_name_adress.get("1.0", tk.END).strip() #Get text from textbox
      problem = ent_problem.get()
      try:
        cost = float(ent_cost.get())
      except ValueError:
        return messagebox.showerror("Error", "Cost must be a number.")
      description = ent_input_description.get("1.0", tk.END).strip() #Get text from textbox

      if not all([system, system_type, system_model, input_name, tel, code_meli]):
        return messagebox.showerror("Error", "Please fill in all required fields.")
      if not validate_phone(tel):
        return messagebox.showerror("Error","Invalid phone number.")
      if not validate_code_meli(code_meli):
        return messagebox.showerror("Error","Invalid code meli.")

      data_tuple = (arrival, departure, system, system_type, system_model, system_serial, input_name, tel, code_meli, tel_sabet, adress, problem, cost, description)
      result = insert_data(data_tuple)
      if isinstance(result, bool) and result: #Check if insert_data returned True(success)
        messagebox.showinfo("Success", "Data saved successfully!")
      else:
        messagebox.showerror("Error", result) #Show specific error message
    except Exception as e:
      messagebox.showerror("Error", f"An unexpected error occurred: {e}")
      dashbord()
  #...(rest of your paziresh_ function)

