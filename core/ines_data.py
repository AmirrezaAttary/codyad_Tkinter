import sqlite3
from db_pz import db_tel
def insert_data(data):
  try:
    conn = sqlite3.connect('pz.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO paziresh (arrival, departure, system, system_type, system_model, system_serial, input_name, tel, code_meli, tel_sabet, adress, problem, cost, description, Warranty, Warranty_modat, Technician_opinion, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
    return True
  except sqlite3.Error as e:
    print(f"Database error: {e}") # More informative error message
    return False
  

def update_data(id_,data):
    print(id_)
    print(data)
    try:
        conn = sqlite3.connect('pz.db')
        cursor = conn.cursor()
        cursor.execute(f"UPDATE paziresh SET (arrival, departure, system, system_type, system_model, system_serial, input_name, tel, code_meli, tel_sabet, adress, problem, cost, description, Warranty, Warranty_modat, Technician_opinion, status) = ({data}) WHERE id={id_}")
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}") # More informative error message
        return False

def insert_tel(numb):  # numb is now a list of phone numbers
    db_tel()
    try:
        conn = sqlite3.connect('pz.db')
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO PHONE (tel) VALUES (?)", [(num,) for num in numb]) #Create tuples for each number
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False