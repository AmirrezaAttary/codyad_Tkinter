import tkinter as tk
import customtkinter
from customtkinter import *
from persiantools.jdatetime import JalaliDate
import sqlite3
from tkinter import messagebox
import re
from kavenegar import *

##################################################################################
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
      tel TEXT, # Changed to TEXT to accommodate various phone number formats
      code_meli TEXT, # Changed to TEXT to accommodate various national code formats
      tel_sabet TEXT, # Changed to TEXT to accommodate various phone number formats
      adress TEXT,
      problem TEXT,
      cost REAL, # Changed to REAL to allow for decimal values
      description TEXT
    )
  ''')
  conn.commit()
  conn.close()

def insert_data(data):
  try:
    conn = sqlite3.connect('pz.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO paziresh (arrival, departure, system, system_type, system_model, system_serial, input_name, tel, code_meli, tel_sabet, adress, problem, cost, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
    return True
  except sqlite3.Error as e:
    print(f"Database error: {e}") # More informative error message
    return False

def validate_phone(phone_number):
  #Basic phone number validation (adjust regex as needed)
  pattern = r"^\+?\d{10,15}$" #Example: Accepts numbers starting with optional +, min 10 digits
  return bool(re.match(pattern, phone_number))

def validate_code_meli(code_meli):
  #Basic code meli validation (Adjust if needed)
  pattern = r"^\d{10}$" # Example: 10 digits
  return bool(re.match(pattern, code_meli))


DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("dark-blue")

##########################################################################################
root = CTk()
root.iconbitmap('tv.ico')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure((0, 1, 2, 3), weight=0)
root.grid_rowconfigure((4, 5, 6, 7), weight=1)
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
api = KavenegarAPI("3936466A51684633482B34396E5541532F66585A455958385036674E54796A52694530396A48766E6574413D")
font = CTkFont(family="Vazir",size=25,weight='bold')
font_enry=CTkFont(family="Vazir",size=20)
#########################################################################################

def clear_frame():
  for widget in root.winfo_children():
    widget.destroy()
def close_window(): 
    root.destroy()
    
def dashbord():
    clear_frame()
    far = CTkFrame(root)
    far.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far.grid_columnconfigure(0, weight=1)
    # far.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
    far.grid_rowconfigure(( 0, 1, 2, 3, 4,5, 6,), weight=1)
    bt_dashboard = customtkinter.CTkButton(far, text="پذیرش",font=font, command=paziresh_)
    bt_dashboard.grid(row=1 ,column=0, padx=20, pady=20)

    bt_sms = customtkinter.CTkButton(far, text="گارانتی",font=font, command=garanti)
    bt_sms.grid(row=2 ,column=0, padx=20, pady=20)

    bt_sms = customtkinter.CTkButton(far, text="ارسال پیامک",font=font, command=send_sms)
    bt_sms.grid(row=3 ,column=0, padx=20, pady=20)

    bt_tarikh = customtkinter.CTkButton(far, text="تاریخچه",font=font, command=tarikh_)
    bt_tarikh.grid(row=4 ,column=0, padx=20, pady=20)
    

    btn_quit = customtkinter.CTkButton(far, text="خروج", fg_color= '#EA0000', hover_color = '#B20000',font=font, command= close_window)
    btn_quit.grid(row=5, column=0, padx=20, pady=0)



try:
    conn = sqlite3.connect('pz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM paziresh")
    result = cursor.fetchone()
    b = result[0] + 1 if result[0] is not None else 1
    print(b)
    conn.close()
except Exception as e:
    messagebox.showerror("Error", f"An error occurred while getting the next ID: {e}")
    b = 1 #Default to 1 if there is an error

def paziresh_():
    clear_frame()
    
    def save_data():
        try:
            arrival = ent_date_of_arrival.get()
            departure = ent_departure_date.get()
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
        
    far_2 = CTkFrame(root)
    far_2.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_2.grid_columnconfigure((0,1,2,3,4,5), weight=1)
    far_2.grid_rowconfigure((0, 1, 2, 3), weight=1)
    far_2.grid_rowconfigure((4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,), weight=1)
    bt_back = customtkinter.CTkButton(far_2, text="بازگشت",font=font, fg_color= '#EA0000', hover_color = '#B20000', command=dashbord)
    bt_back.grid(row=13, column=0, padx=20, pady=(10, 0),sticky=E)

    bt_save = customtkinter.CTkButton(far_2, text="بازگشت و ذخیره",font=font,fg_color="green",hover_color="#00ff00", command=save_data)
    bt_save.grid(row=13, column=1, padx=20, pady=(10, 0),)
    
    lbl_id = CTkLabel(far_2, font=font,text=": شماره پذریش ")
    lbl_id.grid(row=0, column=5,pady=5)
    lbl_1 = CTkLabel(far_2, text="مشخصات دستگاه",font=font,corner_radius=20)
    lbl_1.grid(row=1,column=5,sticky=E,padx=10,pady=5)
    ent_input_id = CTkEntry(far_2,font=font_enry,justify=RIGHT)
    ent_input_id.grid(row=0, column=4)
    ent_input_id.insert(0,b)
    ent_input_id.configure(state=DISABLED)
    
    lbl_date_of_arrival = CTkLabel(far_2, font=font,text=" : تاریخ ورود")
    lbl_date_of_arrival.grid(row=0, column=3,pady=5)
    ent_date_of_arrival = CTkEntry(far_2,font=font_enry,justify=RIGHT)
    ent_date_of_arrival.grid(row=0, column=2,pady=5)
    ent_date_of_arrival.insert(0,JalaliDate.today().strftime('%Y/%m/%d'))
    lbl_departure_date = CTkLabel(far_2, font=font,text=" : تاریخ خروج")
    lbl_departure_date.grid(row=0, column=1,pady=5)
    ent_departure_date = CTkEntry(far_2,font=font_enry)
    ent_departure_date.grid(row=0, column=0,pady=5)
    #########################################################################################
    frame_top = CTkFrame(far_2)
    frame_top.grid(row=2,column=0,columnspan=6,rowspan=3,sticky=NSEW) 
    frame_top.grid_columnconfigure((0,1,2,3,4,5),weight=1)
    frame_top.grid_rowconfigure((0,1),weight=1)
    lbl_input_system = CTkLabel(frame_top,text=" : نام دستگاه",font=font)
    lbl_input_system.grid(row=0,column=5)
    ent_input_system = CTkEntry(frame_top,font=font,justify=RIGHT)
    ent_input_system.grid(row=0,column=4)
    lbl_input_system_type = CTkLabel(frame_top,text=" : نوع دستگاه",font=font)
    lbl_input_system_type.grid(row=0,column=3)
    tv_list = ['LCD','LED','PLOSMA']
    combo_input_system_type = CTkComboBox(frame_top,font=font_enry,values=tv_list)
    combo_input_system_type.grid(row=0,column=2)
    lbl_input_system_model = CTkLabel(frame_top,text=" : مدل دستگاه",font=font)
    lbl_input_system_model.grid(row=0,column=1)
    ent_input_system_model = CTkEntry(frame_top,font=font,justify=RIGHT)
    ent_input_system_model.grid(row=0,column=0)
    lbl_input_system_serial = CTkLabel(frame_top,text=" : سریال دستگاه",font=font)
    lbl_input_system_serial.grid(row=1,column=5)
    ent_input_system_serial = CTkEntry(frame_top,font=font,justify=RIGHT)
    ent_input_system_serial.grid(row=1,column=4)
    #########################################################################
    lbl_2 = CTkLabel(far_2, text="مشخصات مالک",font=font)
    lbl_2.grid(row=5,column=5,sticky=E,padx=10)
    frame_down = CTkFrame(far_2,)
    frame_down.grid(row=6,column=0,columnspan=6,rowspan=3,sticky=NSEW) 
    frame_down.grid_columnconfigure((0,1,2,3,4,5),weight=1)
    frame_down.grid_rowconfigure((0,1),weight=1)
    lbl_input_name = CTkLabel(frame_down,text=" : نام مالک",font=font)
    lbl_input_name.grid(row=0,column=5)
    ent_input_name = CTkEntry(frame_down,font=font_enry,justify=RIGHT)
    ent_input_name.grid(row=0,column=4)
    lbl_input_name_tel = CTkLabel(frame_down,text=" : شماره تلفن",font=font)
    lbl_input_name_tel.grid(row=0,column=3)
    ent_input_name_tel = CTkEntry(frame_down,font=font_enry,justify=LEFT)
    ent_input_name_tel.grid(row=0,column=2)
    lbl_input_name_code_meli = CTkLabel(frame_down,text=" : کد ملی ",font=font)
    lbl_input_name_code_meli.grid(row=0,column=1)
    ent_input_name_code_meli = CTkEntry(frame_down,font=font_enry,justify=LEFT)
    ent_input_name_code_meli.grid(row=0,column=0)
    lbl_input_name_tel_sabet = CTkLabel(frame_down,text=" : تلفن ثابت",font=font)
    lbl_input_name_tel_sabet.grid(row=1,column=5)
    ent_input_name_tel_sabet = CTkEntry(frame_down,font=font_enry,justify=RIGHT)
    ent_input_name_tel_sabet.grid(row=1,column=4)
    lbl_input_name_adress = CTkLabel(frame_down,text=" : آدرس ",font=font)
    lbl_input_name_adress.grid(row=1,column=3)
    ent_input_name_adress = CTkTextbox(frame_down,font=font,corner_radius=10,width=600,border_width=3)
    ent_input_name_adress.tag_config("rtl",justify=RIGHT)
    ent_input_name_adress.tag_add("rtl",0.0,END)
    ent_input_name_adress.insert(0.0,'استان\n','rtl')
    ent_input_name_adress.grid(row=1,column=0,columnspan=2,)
    #############################################################################
    lbl_3 = CTkLabel(far_2, text="مشخصات مشکل",font=font)
    lbl_3.grid(row=9,column=5,sticky=E,padx=10)
    frame_moshkel = CTkFrame(far_2)
    frame_moshkel.grid(row=10,column=0,columnspan=6,rowspan=3,sticky=NSEW) 
    frame_moshkel.grid_columnconfigure((0,1,2,3,),weight=1)
    frame_moshkel.grid_rowconfigure((0,1),weight=1)
    lbl_problem = CTkLabel(frame_moshkel,text=' : ایراد ظاهری',font=font)
    lbl_problem.grid(row=0,column=3,)
    ent_problem = CTkEntry(frame_moshkel,font=font_enry,justify=RIGHT)
    ent_problem.grid(row=0,column=2)
    lbl_cost = CTkLabel(frame_moshkel,text=' : هزینه ',font=font)
    lbl_cost.grid(row=0,column=1,)
    ent_cost = CTkEntry(frame_moshkel,font=font_enry,justify=RIGHT)
    ent_cost.grid(row=0,column=0)
    ent_cost.insert(0,0)
    lbl_input_description = CTkLabel(frame_moshkel,text=" : توضیحات ",font=font)
    lbl_input_description.grid(row=1,column=3)
    ent_input_description = CTkTextbox(frame_moshkel,font=font,corner_radius=10,width=700,border_width=3)
    ent_input_description.tag_config("rtl",justify=RIGHT)
    ent_input_description.tag_add("rtl",0.0,END)
    ent_input_description.insert(0.0,'شکستگی\n','rtl')
    ent_input_description.grid(row=1,column=0,columnspan=3,)
    ########################################################################################
    
    
    
    
    
def garanti():
    far_4 = CTkFrame(root)
    far_4.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_4.grid_columnconfigure(0, weight=1)
    far_4.grid_rowconfigure((0, 1, 2, 3), weight=1)
    far_4.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_4, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=7, column=0, padx=20, pady=(10, 0))
    farame_garanti = CTkFrame(far_4,)
    farame_garanti.grid(row=0, column=0,rowspan=7, sticky=NSEW,padx=20,pady=20)
    

def send_sms():
    def taki():
        
        try:
            params = {
                'receptor':f"{ent_sms_taki.get()}", #Recipient phone number
                'sender': '2000500666',    # Your Kavenegar sender ID
                'message': '''با سلام
کالا های شما در 
شرکت قادری تعمیر و 
آماده تحویل است.''',
            }
            response = api.sms_send(params)
            print(response) # Check the response from the API
        except APIException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        dashbord()
        
    far_3 = CTkFrame(root)
    far_3.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_3.grid_columnconfigure(0, weight=1)
    far_3.grid_rowconfigure((0, 1, 2, 3,4, 5, 6, 7, 8, 9, 10), weight=1)
    lbl_sms = CTkLabel(far_3,text='ارسال تکی',font=font)
    lbl_sms.grid(row=0, column=0 ,padx=20,pady=10)
    frame_send_taki = CTkFrame(far_3,width=300,height=300)
    frame_send_taki.grid(row=1,column=0,rowspan=3,padx=20,)
    lbl_sms_taki = CTkLabel(frame_send_taki,text=': شماره مورد نظر',font=font)
    lbl_sms_taki.pack(pady=25,padx=25)
    ent_sms_taki = CTkEntry(frame_send_taki,font=font_enry)
    ent_sms_taki.pack(pady=25,padx=25)
    but_sms_taki = CTkButton(frame_send_taki,text='ارسال',font=font,fg_color="green",hover_color="#009933", command=taki)
    but_sms_taki.pack(pady=25,padx=25)
    
    ####################################################################################
    lbl_sms_koli = CTkLabel(far_3,text='ارسال گروهی',font=font)
    lbl_sms_koli.grid(row=4, column=0 ,padx=20,pady=10)
    frame_send_koli = CTkFrame(far_3)
    frame_send_koli.grid(row=5,column=0,rowspan=3,padx=20,pady=5)
    bt_from_frame3 = customtkinter.CTkButton(far_3, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=9, column=0, padx=20, pady=(10, 0))
    

def tarikh_():
    far_4 = CTkFrame(root)
    far_4.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_4.grid_columnconfigure(0, weight=1)
    far_4.grid_rowconfigure((0, 1, 2, 3), weight=0)
    far_4.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_4, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=7, column=0, padx=20, pady=(10, 0))
    
    
def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
def setting():
    far_5 = CTkFrame(root)
    far_5.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_5.grid_columnconfigure(0, weight=1)
    far_5.grid_rowconfigure((0, 1, 2, 3), weight=1)
    far_5.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_5, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=7, column=0, padx=20, pady=(10, 0))
    scaling_label = customtkinter.CTkLabel(far_5, text="UI Scaling:", anchor="w")
    scaling_label.grid(row=4, column=0, padx=20, pady=(10, 0))
    scaling_optionemenu = customtkinter.CTkOptionMenu(root, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=change_scaling_event)
    scaling_optionemenu.grid(row=5, column=0, padx=20, pady=(10, 20))

###########################################################################################
far = CTkFrame(root)
far.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
far.grid_columnconfigure(0, weight=1)
# far.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
far.grid_rowconfigure(( 0, 1, 2, 3, 4, 5, 6, ), weight=1)

bt_dashboard = customtkinter.CTkButton(far, text="پذیرش",font=font, command=paziresh_)
bt_dashboard.grid(row=1 ,column=0, padx=20, pady=20)

bt_sms = customtkinter.CTkButton(far, text="گارانتی",font=font, command=garanti)
bt_sms.grid(row=2 ,column=0, padx=20, pady=20)

bt_sms = customtkinter.CTkButton(far, text="ارسال پیامک",font=font, command=send_sms)
bt_sms.grid(row=3 ,column=0, padx=20, pady=20)

bt_tarikh = customtkinter.CTkButton(far, text="تاریخچه",font=font, command=tarikh_)
bt_tarikh.grid(row=4 ,column=0, padx=20, pady=20)



btn_quit = customtkinter.CTkButton(far, text="خروج", fg_color= '#EA0000', hover_color = '#B20000',font=font, command= close_window)
btn_quit.grid(row=5, column=0, padx=20, pady=0)


root.mainloop()