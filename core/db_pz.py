import sqlite3
def create_database():
  conn = sqlite3.connect('database/pz.db')
  cursor = conn.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS paziresh
                (id INTEGER PRIMARY KEY,
                arrival varchar(20) NOT NULL,
                departure varchar(20) ,
                system varchar(20) NOT NULL,
                system_type varchar(20) NOT NULL,
                system_model varchar(20) NOT NULL,
                system_serial varchar(20) NOT NULL,
                input_name varchar(20) NOT NULL,
                tel INTEGER(10) NOT NULL,
                code_meli INTEGER(11) NOT NULL,
                tel_sabet INTEGER(10) ,
                adress varchar(200) NOT NULL,
                problem varchar(20) NOT NULL,
                cost INTEGER(100) ,
                description varchar(200) NOT NULL,
                Warranty varchar(20) NOT NULL,
                Warranty_modat INTEGER(3),
                Technician_opinion varchar(200) NOT NULL,
                status INTEGER(1) NOT NULL)''')
  conn.commit()
  conn.close()

def db_tel():
    conn = sqlite3.connect('database/pz.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS PHONE
                    (id INTEGER PRIMARY KEY,
                    tel INTEGER(11) NOT NULL)''')
    conn.commit()
    conn.close()
    
    
    
def create_settings_table():
    conn = sqlite3.connect("database/pz.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sms_settings (
            id INTEGER PRIMARY KEY,
            sender_number TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
    
def save_sender_number(number):
    conn = sqlite3.connect("database/pz.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sms_settings")  # فقط یک شماره ذخیره می‌کنیم
    cursor.execute("INSERT INTO sms_settings (sender_number) VALUES (?)", (number,))
    conn.commit()
    conn.close()


def get_sender_number():
    conn = sqlite3.connect("database/pz.db")
    cursor = conn.cursor()
    cursor.execute("SELECT sender_number FROM sms_settings LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else '200060006069'  # مقدار پیش‌فرض
