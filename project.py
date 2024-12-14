import customtkinter
from customtkinter import *
from persiantools.jdatetime import JalaliDate
import sqlite3
from tkinter import messagebox
import re
from kavenegar import *
import jinja2
import pdfkit
import time

##################################################################################
def create_database():
  conn = sqlite3.connect('pz.db')
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

create_database()

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

def validate_phone(phone_number):
  #Basic phone number validation (adjust regex as needed)
  pattern = r"^\+?\d{11}$" #Example: Accepts numbers starting with optional +, min 10 digits
  return bool(re.match(pattern, phone_number))

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



def validate_code_meli(code_meli):
  #Basic code meli validation (Adjust if needed)
  pattern = r"^\d{10}$" # Example: 10 digits
  return bool(re.match(pattern, code_meli))

def db_tel():
    conn = sqlite3.connect('pz.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS PHONE
                    (id INTEGER PRIMARY KEY,
                    tel INTEGER(11) NOT NULL)''')
    conn.commit()
    conn.close()

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

DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("dark-blue")

##########################################################################################
root = CTk()
root.iconbitmap('tv.ico')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure((0, 1, 2, 3), weight=0)
root.grid_rowconfigure((4, 5, 6, 7), weight=1)
# root.overrideredirect(True)
root.title('Behroz Electronic')
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
api = KavenegarAPI("742F364166354D7762516C617272357A545936513567685A5064344851557141504D726D65645A337132493D")
font = CTkFont(family="Vazir",size=25,weight='bold')
font_enry=CTkFont(family="Vazir",size=20)
#########################################################################################


def taki(number):
        print(number)
        try:
            params = {
                'receptor':f"{number}", #Recipient phone number
                'sender': '200060006069',    # Your Kavenegar sender ID
                'message': '''با سلام
کالا های شما در 
شرکت قادری تعمیر و 
آماده تحویل است.''',
            }
            response = api.sms_send(params)
            print(response) # Check the response from the API
        except APIException as e:
            return messagebox.showerror("error",f"Error: {e}")
        except Exception as e:
            dashbord()
            return messagebox.showinfo('yes',f"An unexpected error occurred: {e}")
        

def koli(numbers):
        print(numbers)
        try:
            params = {
                'receptor': numbers, #Recipient phone number
                'sender': '200060006069',    # Your Kavenegar sender ID
                'message': '''با سلام
کالا های شما در 
شرکت قادری تعمیر و 
آماده تحویل است.''',
            }
            response = api.sms_send(params)
            print(response) # Check the response from the API
        except APIException as e:
            return messagebox.showerror("error",f"Error: {e}")
        except Exception as e:
            dashbord()
            return messagebox.showinfo('yes',f"An unexpected error occurred: {e}")
        

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
    far.grid_rowconfigure(( 0, 1, 2, 3, 4, 5,), weight=1)
    bt_dashboard = customtkinter.CTkButton(far, text="پذیرش",font=font, command=paziresh_)
    bt_dashboard.grid(row=1 ,column=0, padx=20, pady=20)


    bt_sms = customtkinter.CTkButton(far, text="ارسال پیامک",font=font, command=send_sms)
    bt_sms.grid(row=2 ,column=0, padx=20, pady=20)



    bt_tarikh = customtkinter.CTkButton(far, text="تاریخچه",font=font, command=tarikh_)
    bt_tarikh.grid(row=3 ,column=0, padx=20, pady=20)
    

    btn_quit = customtkinter.CTkButton(far, text="خروج", fg_color= '#EA0000', hover_color = '#B20000',font=font, command= close_window)
    btn_quit.grid(row=4, column=0, padx=20, pady=0)


def paziresh_():
    create_database()
    clear_frame()
    try:
        conn = sqlite3.connect('pz.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM paziresh")
        result = cursor.fetchone()
        b = result[0] + 1 if result[0] is not None else 1
        b+=1590
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while getting the next ID: {e}")
    
    
    def save_data():
        
        try:
            arrival = ent_date_of_arrival.get()
            departure = ent_departure_date.get()
            system = ent_input_system.get()
            system_type = combo_input_system_type.get()
            system_model = ent_input_system_model.get()
            try:
                system_serial = str(ent_input_system_serial.get())
            except ValueError:
                return messagebox.showerror("Error", "Serial number must be an integer.")
            input_name = ent_input_name.get()
            tel = ent_input_name_tel.get()
            code_meli = ent_input_name_code_meli.get()
            tel_sabet = ent_input_name_tel_sabet.get()
            adress = ent_input_name_adress.get("1.0", END).strip() #Get text from textbox
            problem = ent_problem.get("1.0", END).strip()
            try:
                cost = float(ent_cost.get())
            except ValueError:
                return messagebox.showerror("Error", "Cost must be a number.")
            description = ent_input_description.get("1.0", END).strip() #Get text from textbox
            Warrantyy = chek.get() 
            Warrantyy_mod = ent_modat_garanti.get()
            op_tek = ent_tak.get(0.0,END)
            status = chek_exit.get()
            if not all([system, system_type, system_model, input_name, tel, code_meli]):
                return messagebox.showerror("Error", "Please fill in all required fields.")
            if not validate_phone(tel):
                return messagebox.showerror("Error","Invalid phone number.")
            if not validate_code_meli(code_meli):
                return messagebox.showerror("Error","Invalid code meli.")

            data_tuple = (arrival, departure, system, system_type, system_model, system_serial, input_name, tel, code_meli, tel_sabet, adress, problem, cost, description,Warrantyy,Warrantyy_mod,op_tek,status)
            result = insert_data(data_tuple)
            if isinstance(result, bool) and result: #Check if insert_data returned True(success)
                messagebox.showinfo("Success", "Data saved successfully!")
            else:
                messagebox.showerror("Error", result) #Show specific error message
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        dashbord()
        
    def save_data_print():
        
        try:
            arrival = ent_date_of_arrival.get()
            departure = ent_departure_date.get()
            system = ent_input_system.get()
            system_type = combo_input_system_type.get()
            system_model = ent_input_system_model.get()
            try:
                system_serial = str(ent_input_system_serial.get())
            except ValueError:
                return messagebox.showerror("Error", "Serial number must be an integer.")
            input_name = ent_input_name.get()
            tel = ent_input_name_tel.get()
            code_meli = ent_input_name_code_meli.get()
            tel_sabet = ent_input_name_tel_sabet.get()
            adress = ent_input_name_adress.get("1.0", END).strip() #Get text from textbox
            problem = ent_problem.get("1.0", END).strip()
            try:
                cost = float(ent_cost.get())
            except ValueError:
                return messagebox.showerror("Error", "Cost must be a number.")
            description = ent_input_description.get("1.0", END).strip() #Get text from textbox
            Warrantyy = chek.get() 
            Warrantyy_mod = ent_modat_garanti.get()
            op_tek = ent_tak.get(0.0,END)
            status = chek_exit.get()
            if not all([system, system_type, system_model, input_name, tel, code_meli]):
                return messagebox.showerror("Error", "Please fill in all required fields.")
            if not validate_phone(tel):
                return messagebox.showerror("Error","Invalid phone number.")
            if not validate_code_meli(code_meli):
                return messagebox.showerror("Error","Invalid code meli.")

            data_tuple = (arrival, departure, system, system_type, system_model, system_serial, input_name, tel, code_meli, tel_sabet, adress, problem, cost, description,Warrantyy,Warrantyy_mod,op_tek,status)
            result = insert_data(data_tuple)
            if isinstance(result, bool) and result: #Check if insert_data returned True(success)
                messagebox.showinfo("Success", "Data saved successfully!")
                curr_time = time.strftime("%H:%M:%S", time.localtime())
                context = {
                    'id':ent_input_id.get(),
                'garanti':chek.get(),
                'tarikh':ent_date_of_arrival.get(),
                'date':curr_time,
                'name_input':ent_input_name.get(),
                'system_name':ent_input_system.get(),
                'typee':combo_input_system_type.get(),
                'model':ent_input_system_model.get(),
                'seriyal':ent_input_system_serial.get(),
                'tel':ent_input_name_tel.get(),
                'addres':ent_input_name_adress.get("1.0", END),
                'moshkel':ent_input_description.get("1.0", END),
                'modat' : ent_modat_garanti.get()
                }
                temp_loder = jinja2.FileSystemLoader('./template/')
                temp_env = jinja2.Environment(loader=temp_loder)
                temp = temp_env.get_template('atar.html')
                output_text = temp.render(context)
                # Replace with your path
                config = pdfkit.configuration(wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
                pdfkit.from_string(output_text,f'./print/sefaresh_{ent_input_id.get()}.pdf',options={"encoding":'UTF-8','page-width': 210,'page-height': 151},configuration=config,)
                messagebox.showinfo("چاپ",'رسید پرینت شد')
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

    bt_save = customtkinter.CTkButton(far_2, text="ذخیره",font=font,fg_color="green",hover_color="#00ff00", command=save_data)
    bt_save.grid(row=13, column=1, padx=20, pady=(10, 0),)
    
    bt_save = customtkinter.CTkButton(far_2, text="ذخیره و پرینت",font=font,fg_color="green",hover_color="#00ff00", command=save_data_print)
    bt_save.grid(row=13, column=2, padx=20, pady=(10, 0),sticky=W)
    
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
    lbl_input_name_code_meli.grid(row=0,column=1,sticky=W)
    ent_input_name_code_meli = CTkEntry(frame_down,font=font_enry,justify=LEFT)
    ent_input_name_code_meli.grid(row=0,column=0,sticky=E)
    lbl_input_name_tel_sabet = CTkLabel(frame_down,text=" : تلفن ثابت",font=font)
    lbl_input_name_tel_sabet.grid(row=1,column=5)
    ent_input_name_tel_sabet = CTkEntry(frame_down,font=font_enry,justify=RIGHT)
    ent_input_name_tel_sabet.grid(row=1,column=4)
    lbl_input_name_adress = CTkLabel(frame_down,text=" : آدرس ",font=font)
    lbl_input_name_adress.grid(row=1,column=2,sticky=W)
    ent_input_name_adress = CTkTextbox(frame_down,font=font,corner_radius=10,width=400,height=100,border_width=3)
    ent_input_name_adress.tag_config("rtl",justify=RIGHT)
    ent_input_name_adress.tag_add("rtl",0.0,END)
    ent_input_name_adress.insert(0.0,'استان\n','rtl')
    ent_input_name_adress.grid(row=1,column=0,columnspan=2)
    #############################################################################
    lbl_3 = CTkLabel(far_2, text="مشخصات مشکل",font=font)
    lbl_3.grid(row=9,column=5,sticky=E,padx=10)
    frame_moshkel = CTkFrame(far_2)
    frame_moshkel.grid(row=10,column=0,columnspan=6,rowspan=3,sticky=NSEW) 
    frame_moshkel.grid_columnconfigure((0,1,2,3,4),weight=1)
    frame_moshkel.grid_rowconfigure((0,1,2),weight=1)
    lbl_problem = CTkLabel(frame_moshkel,text=' : ایراد ظاهری',font=font)
    lbl_problem.grid(row=0,column=3,)
    ent_problem = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)
    ent_problem.grid(row=0,column=2,sticky=E)
    ent_problem.tag_config('rtl',justify=RIGHT)
    ent_problem.tag_add('rtl',0.0,END)
    ent_problem.insert(0.0,'شکستگی\n','rtl')
    lbl_cost = CTkLabel(frame_moshkel,text=' : هزینه ',font=font)
    lbl_cost.grid(row=0,column=1,sticky=E)
    ent_cost = CTkEntry(frame_moshkel,font=font_enry,justify=RIGHT)
    ent_cost.grid(row=0,column=0,sticky=E)
    ent_cost.insert(0,0)
    lbl_input_description = CTkLabel(frame_moshkel,text=" : توضیحات ",font=font)
    lbl_input_description.grid(row=1,column=3)
    ent_input_description = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)
    ent_input_description.tag_config("rtl",justify=RIGHT)
    ent_input_description.tag_add("rtl",0.0,END)
    ent_input_description.insert(0.0,'شکستگی\n','rtl')
    ent_input_description.grid(row=1,column=2,sticky=E)
    lbl_tak = CTkLabel(frame_moshkel,text=": نظر تکنسین",font=font)
    lbl_tak.grid(row=2,column=3)
    ent_tak = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)
    ent_tak.tag_config("rtl",justify=RIGHT)
    ent_tak.tag_add("rtl",0.0,END)
    ent_tak.insert(0.0,'شکستگی\n','rtl')
    ent_tak.grid(row=2,column=2,sticky=E,)
    lbl_chek = CTkLabel(frame_moshkel,0,28,font=font,text="آیاگارانتی دارد؟")
    lbl_chek.grid(row=1,column=1,sticky=E)
    lbl_modat_garanti =CTkLabel(frame_moshkel,font=font,text="مدت گارنتی",)
    lbl_modat_garanti.grid(row=2,column=1,sticky=NE,)
    ent_modat_garanti =CTkEntry(frame_moshkel,placeholder_text="مدت گارانتی",font=font_enry,justify=CENTER,state=DISABLED)
    ent_modat_garanti.grid(row=2,column=1,sticky=E,)
    def modat():
        if chek.get() == "بلی":
            ent_modat_garanti.configure(placeholder_text="مدت گارانتی",state=NORMAL)
        elif chek.get() == "خیر":
            ent_modat_garanti.configure(placeholder_text="مدت گارانتی",state=DISABLED)
    
    chek_exit = CTkCheckBox(frame_moshkel,text="آماده تحویل",font=font,onvalue=1,offvalue=0)
    chek_exit.grid(row=2,column=0,sticky=E)
    
    abbbb = ''
    str_ = StringVar(value=abbbb)
    chek = CTkCheckBox(frame_moshkel,30,text="بلی",font=font,onvalue="بلی",offvalue="خیر",variable=str_,command=modat)
    chek.grid(row=1,column=0,sticky=E)
    chek_2 = CTkCheckBox(frame_moshkel,text="خیر",font=font,onvalue="خیر",offvalue="بلی",variable=str_,command=modat)
    chek_2.grid(row=1,column=0,)
    



def send_sms():
    db_tel()
    con = sqlite3.connect("pz.db")
    c = con.cursor()
    list_jam = []
    list_person_name = []
    for p in c.execute('SELECT tel FROM paziresh '):
        a = list(p)
        list_person_name.append(a)
    list_person_name_2 = []
    list_person_name_2_str = []
    for i in list_person_name:
        a= int(i[0])
        list_person_name_2.append(a)
        list_person_name_2_str.append(f'0{a}')
        list_jam.append(f'0{a}')
        
    list_afzode = []
    list_afzode_str = []
    for l in c.execute('SELECT tel FROM PHONE '):
        n = int(l[0])
        list_afzode.append(n)
        list_afzode_str.append(f'0{n}')
        list_jam.append(f'0{n}')
    con.commit()
    con.close()
    
    
    
    def sel_taki():
        
        def get__():
            print(ent_sms_taki.get())
            numb=ent_sms_taki.get() 
            taki(numb)
        lbl_sms = CTkLabel(far_3,height=10,text='ارسال تکی',font=font)
        lbl_sms.grid(row=0, column=0 ,padx=20,pady=10)
        frame_send_taki = CTkFrame(far_3,width=300,height=200)
        frame_send_taki.grid(row=1,column=0,rowspan=3,padx=20,)
        frame_send_taki.grid_columnconfigure(0,weight=1)
        frame_send_taki.grid_rowconfigure((0,1,2),weight=1)
        lbl_sms_taki = CTkLabel(frame_send_taki,text=': شماره مورد نظر',font=font)
        lbl_sms_taki.grid(row=0,column=0,padx=25)
        ent_sms_taki = CTkEntry(frame_send_taki,font=font_enry)
        ent_sms_taki.grid(row=1,column=0,pady=25,padx=25)
        but_sms_taki = CTkButton(frame_send_taki,text='ارسال',font=font,fg_color="green",hover_color="#009933", command=get__)
        but_sms_taki.grid(row=2,column=0,padx=25)
   
    ####################################################################################
    def sel_koli():
        def clear_kol():
            for widget in sc_3.winfo_children():
                widget.destroy()
        
        frame_send_koli = CTkFrame(far_3,width=300,height=200)
        frame_send_koli.grid(row=5,column=0,rowspan=3,padx=300,pady=5,sticky=NSEW)
        frame_send_koli.grid_columnconfigure((0),weight=1)
        frame_send_koli.grid_rowconfigure((0,1),weight=1)
        tab_w = CTkTabview(frame_send_koli)
        tab_w.add('دستگاه داخل')
        tab_w.add('+افزودن')
        tab_w.add('شده افزوده')
        tab_w.add('شماره همه')
        tab_w.tab('دستگاه داخل').grid_rowconfigure((0,1,2),weight=1)
        tab_w.tab('+افزودن').grid_rowconfigure((0,1,2),weight=1)
        tab_w.tab('شماره همه').grid_rowconfigure((0,1,2),weight=1)
        tab_w.tab('شده افزوده').grid_rowconfigure((0,1,2),weight=1)
        tab_w.tab('دستگاه داخل').grid_columnconfigure(0,weight=1)
        tab_w.tab('+افزودن').grid_columnconfigure(0,weight=1)
        tab_w.tab('شماره همه').grid_columnconfigure(0,weight=1)
        tab_w.tab('شده افزوده').grid_columnconfigure(0,weight=1)
        
        tab_w.grid(row=0,column=0,)
        lbl_sms_koli = CTkLabel(far_3,text='ارسال گروهی',font=font)
        lbl_sms_koli.grid(row=4, column=0 ,padx=20,pady=10)
        list_numb = []
        list_numb_str = []
        def upload_file_1():
            def ins():
                print(list_numb_str)
                insert_tel(list_numb)
                send_sms()
                return messagebox.showinfo('Upload','اطلاعات با موفقیت ذخیره شد')
            clear_kol()
            file_path = filedialog.askopenfilename()
            with open(file_path,'r') as f:
                for line in f:
                    numbb = CTkEntry(sc_3,font=font_enry)
                    numbb.insert(END,f'{line}')
                    numbb.pack()
                    a = int(numbb.get())
                    list_numb.append(a)
                    list_numb_str.append(f'0{a}')
                CTkButton(sc_3,font=font,text="ثبت",command=ins).pack()
            
            
        bn = CTkButton(tab_w.tab('+افزودن'),text='بارگذاری',font=font,command=upload_file_1)
        bn.grid(row=2,column=0)
        
        
        sc = CTkScrollableFrame(tab_w.tab('دستگاه داخل'),300,250,3,3)
        sc.grid(row=0,rowspan=1,column=0)
        sc_2 = CTkScrollableFrame(tab_w.tab('شماره همه'),300,250,3,3)
        sc_2.grid(row=0,rowspan=1,column=0)
        sc_3 = CTkScrollableFrame(tab_w.tab('+افزودن'),300,250,3,3)
        sc_3.grid(row=0,rowspan=1,column=0)
        sc_4 = CTkScrollableFrame(tab_w.tab('شده افزوده'),300,250,3,3)
        sc_4.grid(row=0,rowspan=1,column=0)
        
        for j in list_person_name_2:
            numb = CTkEntry(sc,font=font_enry)
            numb.insert(END,f'0{j}')
            numb.pack()
            numb.configure(state=DISABLED)
        for j in list_person_name_2:
            numb = CTkEntry(sc_2,font=font_enry)
            numb.insert(END,f'0{j}')
            numb.pack()
            numb.configure(state=DISABLED)
        for o in list_afzode:
            numb = CTkEntry(sc_2,font=font_enry)
            numb.insert(END,f'0{o}')
            numb.pack()
            numb.configure(state=DISABLED)
        for x in list_afzode:
            numb = CTkEntry(sc_4,font=font_enry)
            numb.insert(END,f'0{x}')
            numb.pack()
            numb.configure(state=DISABLED)
       
        
        btn_sms_koli = CTkButton(tab_w.tab('دستگاه داخل'),text='ارسال',font=font,fg_color="green",hover_color="#009933",command=lambda numb=list_person_name_2_str: koli(numb))
        btn_sms_koli.grid(row=2,column=0,padx=20,pady=20)
        btn_sms_koli_2 = CTkButton(tab_w.tab('شماره همه'),text='ارسال',font=font,fg_color="green",hover_color="#009933",command=lambda numb=list_jam: koli(numb))
        btn_sms_koli_2.grid(row=2,column=0,padx=20,pady=20)
        btn_sms_koli_3 = CTkButton(tab_w.tab('شده افزوده'),text='ارسال',font=font,fg_color="green",hover_color="#009933",command=lambda numb=list_afzode_str: koli(numb))
        btn_sms_koli_3.grid(row=2,column=0,padx=20,pady=20)
    
    
    
    far_3 = CTkFrame(root)
    far_3.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_3.grid_columnconfigure((0), weight=1)
    far_3.grid_rowconfigure((0, 1, 2, 3,4, 5, 6, 7, 8, 9, 10,11), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_3, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=9, column=0, padx=20, pady=(10, 0))
    sel_taki()
    sel_koli()

def tarikh_():
    def clear_frame_sct():
        for widget in sct.winfo_children():
            widget.destroy()
    def clear_frame_sct_2():
        for widget in sct_2.winfo_children():
            widget.destroy() 
    def clear_frame_sct_3():
        for widget in sct_3.winfo_children():
            widget.destroy() 
            
    def search():
        con = sqlite3.connect("pz.db")
        c = con.cursor()
        if len(search_entry.get()) == 11:
            print(search_entry.get())
            clear_frame_sct()
            s = CTkFrame(sct,border_width=3)
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkEntry(s,63,28,0,font=CTkFont('Vazir',11))
            ent_id.insert(END,'شماره پذیرش')
            ent_id.grid(row=0,column=10,sticky=E)
            ent_sys = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys.insert(END,"مالک دستگاه")
            ent_sys.grid(row=0,column=9,sticky=E,)
            ent_sys_type = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_type.insert(END,"نام دستگاه")
            ent_sys_type.grid(row=0,column=8,sticky=E,)
            ent_sys_model = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_model.insert(END,"مدل دستگاه")
            ent_sys_model.grid(row=0,column=7,sticky=E,)
            ent_sys_serial = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_serial.insert(END,"کدملی")
            ent_sys_serial.grid(row=0,column=6,sticky=E,)
            ent_sys_war = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_war.insert(END,"موبایل")
            ent_sys_war.grid(row=0,column=5,sticky=E,)
            list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
            for sell in list_sel:
                sell.configure(state=DISABLED) 
            for row in c.execute(f'SELECT * FROM paziresh WHERE tel={search_entry.get()} AND status=0'):
                a=row[0]+1590
                s = CTkFrame(sct,border_width=3,fg_color='blue')
                s.pack(pady=3,anchor=E)
                s.grid_columnconfigure([0,1],weight=1)
                s.grid_rowconfigure([0],weight=1)
                ent_id = CTkEntry(s,63,font=font_enry)
                ent_id.insert(END,a)
                ent_id.grid(row=0,column=10,sticky=E)
                ent_sys = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys.insert(END,row[7])
                ent_sys.grid(row=0,column=9,sticky=E,)
                ent_sys_type = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_type.insert(END,row[3])
                ent_sys_type.grid(row=0,column=8,sticky=E,)
                ent_sys_model = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_model.insert(END,row[5])
                ent_sys_model.grid(row=0,column=7,sticky=E,)
                ent_sys_serial = CTkEntry(s,font=font_enry,justify=RIGHT)
                n = f"0{row[9]}"
                ent_sys_serial.insert(END,n)
                ent_sys_serial.grid(row=0,column=6,sticky=E,)
                ent_sys_war = CTkEntry(s,font=font_enry,justify=RIGHT)
                f = f"0{row[8]}"
                ent_sys_war.insert(END,f)
                ent_sys_war.grid(row=0,column=5,sticky=E,)
                btn_show = CTkButton(s,100,font=font,text='نمایش',command=lambda id_num=row[0]: show(id_num))
                btn_show.grid(row=0,column=4,sticky=E,)
                list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
                for sel in list_sel:
                    sel.configure(state=DISABLED)
            con.commit()
            con.close()
        elif len(search_entry.get()) == 10:
            print(search_entry.get())
            clear_frame_sct()
            s = CTkFrame(sct,border_width=3)
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkEntry(s,63,28,0,font=CTkFont('Vazir',11))
            ent_id.insert(END,'شماره پذیرش')
            ent_id.grid(row=0,column=10,sticky=E)
            ent_sys = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys.insert(END,"مالک دستگاه")
            ent_sys.grid(row=0,column=9,sticky=E,)
            ent_sys_type = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_type.insert(END,"نام دستگاه")
            ent_sys_type.grid(row=0,column=8,sticky=E,)
            ent_sys_model = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_model.insert(END,"مدل دستگاه")
            ent_sys_model.grid(row=0,column=7,sticky=E,)
            ent_sys_serial = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_serial.insert(END,"کدملی")
            ent_sys_serial.grid(row=0,column=6,sticky=E,)
            ent_sys_war = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_war.insert(END,"موبایل")
            ent_sys_war.grid(row=0,column=5,sticky=E,)
            
            list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
            for sell in list_sel:
                sell.configure(state=DISABLED) 
            for row in c.execute(f'SELECT * FROM paziresh WHERE code_meli={search_entry.get()} AND status=0'):
                a=row[0]+1590
                s = CTkFrame(sct,border_width=3,fg_color='blue')
                s.pack(pady=3,anchor=E)
                s.grid_columnconfigure([0,1],weight=1)
                s.grid_rowconfigure([0],weight=1)
                ent_id = CTkEntry(s,63,font=font_enry)
                ent_id.insert(END,a)
                ent_id.grid(row=0,column=10,sticky=E)
                ent_sys = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys.insert(END,row[7])
                ent_sys.grid(row=0,column=9,sticky=E,)
                ent_sys_type = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_type.insert(END,row[3])
                ent_sys_type.grid(row=0,column=8,sticky=E,)
                ent_sys_model = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_model.insert(END,row[5])
                ent_sys_model.grid(row=0,column=7,sticky=E,)
                ent_sys_serial = CTkEntry(s,font=font_enry,justify=RIGHT)
                n = f"0{row[9]}"
                ent_sys_serial.insert(END,n)
                ent_sys_serial.grid(row=0,column=6,sticky=E,)
                ent_sys_war = CTkEntry(s,font=font_enry,justify=RIGHT)
                f = f"0{row[8]}"
                ent_sys_war.insert(END,f)
                ent_sys_war.grid(row=0,column=5,sticky=E,)
                btn_show = CTkButton(s,100,font=font,text='نمایش',command=lambda id_num=row[0]: show(id_num))
                btn_show.grid(row=0,column=4,sticky=E,)
                
                list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
                for sel in list_sel:
                    sel.configure(state=DISABLED)
            con.commit()
            con.close()
        elif search_entry.get() == '':
            print(search_entry.get())
            clear_frame_sct()
            sel_()
        else:
            clear_frame_sct()
            sel_()
            return messagebox.showerror("مشکل",".شماره موبایل/کدملی اشتباه است")
        
        
    def search_2():
        con = sqlite3.connect("pz.db")
        c = con.cursor()
        if len(search_entry_2.get()) == 11:
            print(search_entry_2.get())
            clear_frame_sct_2()
            s = CTkFrame(sct_2,border_width=3)
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkEntry(s,63,28,0,font=CTkFont('Vazir',11))
            ent_id.insert(END,'شماره پذیرش')
            ent_id.grid(row=0,column=10,sticky=E)
            ent_sys = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys.insert(END,"مالک دستگاه")
            ent_sys.grid(row=0,column=9,sticky=E,)
            ent_sys_type = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_type.insert(END,"نام دستگاه")
            ent_sys_type.grid(row=0,column=8,sticky=E,)
            ent_sys_model = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_model.insert(END,"مدل دستگاه")
            ent_sys_model.grid(row=0,column=7,sticky=E,)
            ent_sys_serial = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_serial.insert(END,"کدملی")
            ent_sys_serial.grid(row=0,column=6,sticky=E,)
            ent_sys_war = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_war.insert(END,"موبایل")
            ent_sys_war.grid(row=0,column=5,sticky=E,)
            list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
            for sell in list_sel:
                sell.configure(state=DISABLED) 
            for row in c.execute(f'SELECT * FROM paziresh WHERE tel={search_entry_2.get()}'):
                a=row[0]+1590
                s = CTkFrame(sct_2,border_width=3,fg_color='blue')
                s.pack(pady=3,anchor=E)
                s.grid_columnconfigure([0,1],weight=1)
                s.grid_rowconfigure([0],weight=1)
                ent_id = CTkEntry(s,63,font=font_enry)
                ent_id.insert(END,a)
                ent_id.grid(row=0,column=10,sticky=E)
                ent_sys = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys.insert(END,row[7])
                ent_sys.grid(row=0,column=9,sticky=E,)
                ent_sys_type = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_type.insert(END,row[3])
                ent_sys_type.grid(row=0,column=8,sticky=E,)
                ent_sys_model = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_model.insert(END,row[5])
                ent_sys_model.grid(row=0,column=7,sticky=E,)
                ent_sys_serial = CTkEntry(s,font=font_enry,justify=RIGHT)
                n = f"0{row[9]}"
                ent_sys_serial.insert(END,n)
                ent_sys_serial.grid(row=0,column=6,sticky=E,)
                ent_sys_war = CTkEntry(s,font=font_enry,justify=RIGHT)
                f = f"0{row[8]}"
                ent_sys_war.insert(END,f)
                ent_sys_war.grid(row=0,column=5,sticky=E,)
                btn_show = CTkButton(s,100,font=font,text='نمایش',command=lambda id_num=row[0]: show(id_num))
                btn_show.grid(row=0,column=4,sticky=E,)
                list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
                for sel in list_sel:
                    sel.configure(state=DISABLED)
            con.commit()
            con.close()
        elif len(search_entry_2.get()) == 10:
            clear_frame_sct_2()
            s = CTkFrame(sct_2,border_width=3)
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkEntry(s,63,28,0,font=CTkFont('Vazir',11))
            ent_id.insert(END,'شماره پذیرش')
            ent_id.grid(row=0,column=10,sticky=E)
            ent_sys = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys.insert(END,"مالک دستگاه")
            ent_sys.grid(row=0,column=9,sticky=E,)
            ent_sys_type = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_type.insert(END,"نام دستگاه")
            ent_sys_type.grid(row=0,column=8,sticky=E,)
            ent_sys_model = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_model.insert(END,"مدل دستگاه")
            ent_sys_model.grid(row=0,column=7,sticky=E,)
            ent_sys_serial = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_serial.insert(END,"کدملی")
            ent_sys_serial.grid(row=0,column=6,sticky=E,)
            ent_sys_war = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_war.insert(END,"موبایل")
            ent_sys_war.grid(row=0,column=5,sticky=E,)
            list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
            for sell in list_sel:
                sell.configure(state=DISABLED) 
            for row in c.execute(f'SELECT * FROM paziresh WHERE code_meli={search_entry_2.get()}'):
                a=row[0]+1590
                s = CTkFrame(sct_2,border_width=3,fg_color='blue')
                s.pack(pady=3,anchor=E)
                s.grid_columnconfigure([0,1],weight=1)
                s.grid_rowconfigure([0],weight=1)
                ent_id = CTkEntry(s,63,font=font_enry)
                ent_id.insert(END,a)
                ent_id.grid(row=0,column=10,sticky=E)
                ent_sys = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys.insert(END,row[7])
                ent_sys.grid(row=0,column=9,sticky=E,)
                ent_sys_type = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_type.insert(END,row[3])
                ent_sys_type.grid(row=0,column=8,sticky=E,)
                ent_sys_model = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_model.insert(END,row[5])
                ent_sys_model.grid(row=0,column=7,sticky=E,)
                ent_sys_serial = CTkEntry(s,font=font_enry,justify=RIGHT)
                n = f"0{row[9]}"
                ent_sys_serial.insert(END,n)
                ent_sys_serial.grid(row=0,column=6,sticky=E,)
                ent_sys_war = CTkEntry(s,font=font_enry,justify=RIGHT)
                f = f"0{row[8]}"
                ent_sys_war.insert(END,f)
                ent_sys_war.grid(row=0,column=5,sticky=E,)
                btn_show = CTkButton(s,100,font=font,text='نمایش',command=lambda id_num=row[0]: show(id_num))
                btn_show.grid(row=0,column=4,sticky=E,)
                
                list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
                for sel in list_sel:
                    sel.configure(state=DISABLED)
            con.commit()
            con.close()
        elif search_entry_2.get() == '':
            clear_frame_sct_2()
            sel_2()
        else:
            clear_frame_sct_2()
            sel_2()
            return messagebox.showerror("مشکل",".شماره موبایل/کدملی اشتباه است")
    
    def search_3():
        con = sqlite3.connect("pz.db")
        c = con.cursor()
        if len(search_entry_3.get()) == 11:
            clear_frame_sct_3()
            s = CTkFrame(sct_3,border_width=3)
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkEntry(s,63,28,0,font=CTkFont('Vazir',11))
            ent_id.insert(END,'شماره پذیرش')
            ent_id.grid(row=0,column=10,sticky=E)
            ent_sys = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys.insert(END,"مالک دستگاه")
            ent_sys.grid(row=0,column=9,sticky=E,)
            ent_sys_type = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_type.insert(END,"نام دستگاه")
            ent_sys_type.grid(row=0,column=8,sticky=E,)
            ent_sys_model = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_model.insert(END,"مدل دستگاه")
            ent_sys_model.grid(row=0,column=7,sticky=E,)
            ent_sys_serial = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_serial.insert(END,"کدملی")
            ent_sys_serial.grid(row=0,column=6,sticky=E,)
            ent_sys_war = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_war.insert(END,"موبایل")
            ent_sys_war.grid(row=0,column=5,sticky=E,)
            
            list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
            for sell in list_sel:
                sell.configure(state=DISABLED) 
            for row in c.execute(f'SELECT * FROM paziresh WHERE tel={search_entry_3.get()} AND status=1'):
                a=row[0]+1590
                s = CTkFrame(sct_3,border_width=3,fg_color='blue')
                s.pack(pady=3,anchor=E)
                s.grid_columnconfigure([0,1],weight=1)
                s.grid_rowconfigure([0],weight=1)
                ent_id = CTkEntry(s,63,font=font_enry)
                ent_id.insert(END,a)
                ent_id.grid(row=0,column=10,sticky=E)
                ent_sys = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys.insert(END,row[7])
                ent_sys.grid(row=0,column=9,sticky=E,)
                ent_sys_type = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_type.insert(END,row[3])
                ent_sys_type.grid(row=0,column=8,sticky=E,)
                ent_sys_model = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_model.insert(END,row[5])
                ent_sys_model.grid(row=0,column=7,sticky=E,)
                ent_sys_serial = CTkEntry(s,font=font_enry,justify=RIGHT)
                n = f"0{row[9]}"
                ent_sys_serial.insert(END,n)
                ent_sys_serial.grid(row=0,column=6,sticky=E,)
                ent_sys_war = CTkEntry(s,font=font_enry,justify=RIGHT)
                f = f"0{row[8]}"
                ent_sys_war.insert(END,f)
                ent_sys_war.grid(row=0,column=5,sticky=E,)
                btn_show = CTkButton(s,100,font=font,text='نمایش',command=lambda id_num=row[0]: show(id_num))
                btn_show.grid(row=0,column=4,sticky=E,)
                list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
                for sel in list_sel:
                    sel.configure(state=DISABLED)
            con.commit()
            con.close()
        elif len(search_entry_3.get()) == 10:
            print(search_entry_3.get())
            clear_frame_sct_3()
            s = CTkFrame(sct_3,border_width=3)
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkEntry(s,63,28,0,font=CTkFont('Vazir',11))
            ent_id.insert(END,'شماره پذیرش')
            ent_id.grid(row=0,column=10,sticky=E)
            ent_sys = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys.insert(END,"مالک دستگاه")
            ent_sys.grid(row=0,column=9,sticky=E,)
            ent_sys_type = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_type.insert(END,"نام دستگاه")
            ent_sys_type.grid(row=0,column=8,sticky=E,)
            ent_sys_model = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_model.insert(END,"مدل دستگاه")
            ent_sys_model.grid(row=0,column=7,sticky=E,)
            ent_sys_serial = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_serial.insert(END,"کدملی")
            ent_sys_serial.grid(row=0,column=6,sticky=E,)
            ent_sys_war = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
            ent_sys_war.insert(END,"موبایل")
            ent_sys_war.grid(row=0,column=5,sticky=E,)
            
            list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
            for sell in list_sel:
                sell.configure(state=DISABLED) 
            for row in c.execute(f'SELECT * FROM paziresh WHERE code_meli={search_entry_3.get()} AND status=1'):
                a=row[0]+1590
                s = CTkFrame(sct_3,border_width=3,fg_color='blue')
                s.pack(pady=3,anchor=E)
                s.grid_columnconfigure([0,1],weight=1)
                s.grid_rowconfigure([0],weight=1)
                ent_id = CTkEntry(s,63,font=font_enry)
                ent_id.insert(END,a)
                ent_id.grid(row=0,column=10,sticky=E)
                ent_sys = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys.insert(END,row[7])
                ent_sys.grid(row=0,column=9,sticky=E,)
                ent_sys_type = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_type.insert(END,row[3])
                ent_sys_type.grid(row=0,column=8,sticky=E,)
                ent_sys_model = CTkEntry(s,font=font_enry,justify=RIGHT)
                ent_sys_model.insert(END,row[5])
                ent_sys_model.grid(row=0,column=7,sticky=E,)
                ent_sys_serial = CTkEntry(s,font=font_enry,justify=RIGHT)
                n = f"0{row[9]}"
                ent_sys_serial.insert(END,n)
                ent_sys_serial.grid(row=0,column=6,sticky=E,)
                ent_sys_war = CTkEntry(s,font=font_enry,justify=RIGHT)
                f = f"0{row[8]}"
                ent_sys_war.insert(END,f)
                ent_sys_war.grid(row=0,column=5,sticky=E,)
                btn_show = CTkButton(s,100,font=font,text='نمایش',command=lambda id_num=row[0]: show(id_num))
                btn_show.grid(row=0,column=4,sticky=E,)
                list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
                for sel in list_sel:
                    sel.configure(state=DISABLED)
            con.commit()
            con.close()
        elif search_entry_3.get() == '':
            clear_frame_sct_3()
            sel_3()
        else:
            clear_frame_sct_3()
            sel_3()
            return messagebox.showerror("مشکل",".شماره موبایل/کدملی اشتباه است")
            
    
    def sel_():
        
        s = CTkFrame(sct,border_width=3)
        s.pack(pady=3,anchor=E)
        s.grid_columnconfigure([0,1],weight=1)
        s.grid_rowconfigure([0],weight=1)
        ent_id = CTkEntry(s,63,28,0,font=CTkFont('Vazir',11))
        ent_id.insert(END,'شماره پذیرش')
        ent_id.grid(row=0,column=10,sticky=E)
        ent_sys = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys.insert(END,"مالک دستگاه")
        ent_sys.grid(row=0,column=9,sticky=E,)
        ent_sys_type = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_type.insert(END,"نام دستگاه")
        ent_sys_type.grid(row=0,column=8,sticky=E,)
        ent_sys_model = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_model.insert(END,"مدل دستگاه")
        ent_sys_model.grid(row=0,column=7,sticky=E,)
        ent_sys_serial = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_serial.insert(END,"کدملی")
        ent_sys_serial.grid(row=0,column=6,sticky=E,)
        ent_sys_war = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_war.insert(END,"موبایل")
        ent_sys_war.grid(row=0,column=5,sticky=E,)
        list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
        for sell in list_sel:
            sell.configure(state=DISABLED)  
        con = sqlite3.connect("pz.db")
        c = con.cursor()
        for row in c.execute('SELECT * FROM paziresh WHERE status=0'):
            a=row[0]+1590
            s = CTkFrame(sct,border_width=3,fg_color='blue')
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkEntry(s,63,font=font_enry)
            ent_id.insert(END,a)
            ent_id.grid(row=0,column=10,sticky=E)
            ent_sys = CTkEntry(s,font=font_enry,justify=RIGHT)
            ent_sys.insert(END,row[7])
            ent_sys.grid(row=0,column=9,sticky=E,)
            ent_sys_type = CTkEntry(s,font=font_enry,justify=RIGHT)
            ent_sys_type.insert(END,row[3])
            ent_sys_type.grid(row=0,column=8,sticky=E,)
            ent_sys_model = CTkEntry(s,font=font_enry,justify=RIGHT)
            ent_sys_model.insert(END,row[5])
            ent_sys_model.grid(row=0,column=7,sticky=E,)
            ent_sys_serial = CTkEntry(s,font=font_enry,justify=RIGHT)
            n = f"0{row[9]}"
            ent_sys_serial.insert(END,n)
            ent_sys_serial.grid(row=0,column=6,sticky=E,)
            ent_sys_war = CTkEntry(s,font=font_enry,justify=RIGHT)
            f = f"0{row[8]}"
            ent_sys_war.insert(END,f)
            ent_sys_war.grid(row=0,column=5,sticky=E,)
            
            list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
            for sel in list_sel:
                sel.configure(state=DISABLED)
            btn_show = CTkButton(s,100,font=font,text='نمایش',command=lambda id_num=row[0]: show(id_num))
            btn_show.grid(row=0,column=4,sticky=E,)
        con.commit()
        con.close()
    def sel_2():
        s = CTkFrame(sct_2,border_width=3)
        s.pack(pady=3,anchor=E)
        s.grid_columnconfigure([0,1],weight=1)
        s.grid_rowconfigure([0],weight=1)
        ent_id = CTkEntry(s,63,28,0,font=CTkFont('Vazir',11))
        ent_id.insert(END,'شماره پذیرش')
        ent_id.grid(row=0,column=10,sticky=E)
        ent_sys = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys.insert(END,"مالک دستگاه")
        ent_sys.grid(row=0,column=9,sticky=E,)
        ent_sys_type = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_type.insert(END,"نام دستگاه")
        ent_sys_type.grid(row=0,column=8,sticky=E,)
        ent_sys_model = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_model.insert(END,"مدل دستگاه")
        ent_sys_model.grid(row=0,column=7,sticky=E,)
        ent_sys_serial = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_serial.insert(END,"کدملی")
        ent_sys_serial.grid(row=0,column=6,sticky=E,)
        ent_sys_war = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_war.insert(END,"موبایل")
        ent_sys_war.grid(row=0,column=5,sticky=E,)
        list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
        for sell in list_sel:
            sell.configure(state=DISABLED)  
        
        con = sqlite3.connect("pz.db")
        c = con.cursor()
        for row in c.execute('SELECT * FROM paziresh'):
            a=row[0]+1590
            s = CTkFrame(sct_2,border_width=3,fg_color='blue')
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkEntry(s,63,font=font_enry)
            ent_id.insert(END,a)
            ent_id.grid(row=0,column=10,sticky=E)
            ent_sys = CTkEntry(s,font=font_enry,justify=RIGHT)
            ent_sys.insert(END,row[7])
            ent_sys.grid(row=0,column=9,sticky=E,)
            ent_sys_type = CTkEntry(s,font=font_enry,justify=RIGHT)
            ent_sys_type.insert(END,row[3])
            ent_sys_type.grid(row=0,column=8,sticky=E,)
            ent_sys_model = CTkEntry(s,font=font_enry,justify=RIGHT)
            ent_sys_model.insert(END,row[5])
            ent_sys_model.grid(row=0,column=7,sticky=E,)
            ent_sys_serial = CTkEntry(s,font=font_enry,justify=RIGHT)
            n = f"0{row[9]}"
            ent_sys_serial.insert(END,n)
            ent_sys_serial.grid(row=0,column=6,sticky=E,)
            ent_sys_war = CTkEntry(s,font=font_enry,justify=RIGHT)
            f = f"0{row[8]}"
            ent_sys_war.insert(END,f)
            ent_sys_war.grid(row=0,column=5,sticky=E,)
            
            list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
            for sel in list_sel:
                sel.configure(state=DISABLED)
            btn_show = CTkButton(s,100,font=font,text='نمایش',command=lambda id_num=row[0]: show(id_num))
            btn_show.grid(row=0,column=4,sticky=E,)
        con.commit()
        con.close()
        
    def sel_3():
        s = CTkFrame(sct_3,border_width=3)
        s.pack(pady=3,anchor=E)
        s.grid_columnconfigure([0,1],weight=1)
        s.grid_rowconfigure([0],weight=1)
        ent_id = CTkEntry(s,63,28,0,font=CTkFont('Vazir',11))
        ent_id.insert(END,'شماره پذیرش')
        ent_id.grid(row=0,column=10,sticky=E)
        ent_sys = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys.insert(END,"مالک دستگاه")
        ent_sys.grid(row=0,column=9,sticky=E,)
        ent_sys_type = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_type.insert(END,"نام دستگاه")
        ent_sys_type.grid(row=0,column=8,sticky=E,)
        ent_sys_model = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_model.insert(END,"مدل دستگاه")
        ent_sys_model.grid(row=0,column=7,sticky=E,)
        ent_sys_serial = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_serial.insert(END,"کدملی")
        ent_sys_serial.grid(row=0,column=6,sticky=E,)
        ent_sys_war = CTkEntry(s,corner_radius=0,font=font_enry,justify=CENTER)
        ent_sys_war.insert(END,"موبایل")
        ent_sys_war.grid(row=0,column=5,sticky=E,)
        list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
        for sell in list_sel:
            sell.configure(state=DISABLED)  
        con = sqlite3.connect("pz.db")
        c = con.cursor()
        for row in c.execute('SELECT * FROM paziresh WHERE status=1'):
            a=row[0]+1590
            s = CTkFrame(sct_3,border_width=3,fg_color='blue')
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkEntry(s,63,font=font_enry)
            ent_id.insert(END,a)
            ent_id.grid(row=0,column=10,sticky=E)
            ent_sys = CTkEntry(s,font=font_enry,justify=RIGHT)
            ent_sys.insert(END,row[7])
            ent_sys.grid(row=0,column=9,sticky=E,)
            ent_sys_type = CTkEntry(s,font=font_enry,justify=RIGHT)
            ent_sys_type.insert(END,row[3])
            ent_sys_type.grid(row=0,column=8,sticky=E,)
            ent_sys_model = CTkEntry(s,font=font_enry,justify=RIGHT)
            ent_sys_model.insert(END,row[5])
            ent_sys_model.grid(row=0,column=7,sticky=E,)
            ent_sys_serial = CTkEntry(s,font=font_enry,justify=RIGHT)
            n = f"0{row[9]}"
            ent_sys_serial.insert(END,n)
            ent_sys_serial.grid(row=0,column=6,sticky=E,)
            ent_sys_war = CTkEntry(s,font=font_enry,justify=RIGHT)
            f = f"0{row[8]}"
            ent_sys_war.insert(END,f)
            ent_sys_war.grid(row=0,column=5,sticky=E,)
            
            list_sel = [ent_id,ent_sys,ent_sys_type,ent_sys_model,ent_sys_serial,ent_sys_war,]
            for sel in list_sel:
                sel.configure(state=DISABLED)
            btn_show = CTkButton(s,100,font=font,text='نمایش',command=lambda id_num=row[0]: show(id_num))
            btn_show.grid(row=0,column=4,sticky=E,)
        con.commit()
        con.close()
    
    far_4 = CTkFrame(root)
    far_4.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_4.grid_columnconfigure(0, weight=1)
    far_4.grid_rowconfigure((0, 1, 2, 3), weight=0)
    far_4.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_4, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=7, column=0, padx=20, pady=(10, 0))
    farame_garanti = CTkFrame(far_4,)
    farame_garanti.grid(row=0, column=0,rowspan=7, sticky=NSEW,padx=20,pady=20)
    farame_garanti.grid_columnconfigure(0, weight=1)
    farame_garanti.grid_rowconfigure((0, 1, 2, 3), weight=1)
    
    tab_view = CTkTabview(farame_garanti,)
    tab_view.grid(row=0,rowspan=4, column=0, padx=20, pady=20,sticky=NSEW)
    tab_view.add("تعمیر درحال")
    tab_view.add("سفارش همه")
    tab_view.add("تحویل آماده")
    tab_view.tab("تعمیر درحال").grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
    tab_view.tab("تعمیر درحال").grid_columnconfigure((0), weight=1)
    tab_view.tab("سفارش همه").grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
    tab_view.tab("سفارش همه").grid_columnconfigure((0), weight=1)
    tab_view.tab("تحویل آماده").grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
    tab_view.tab("تحویل آماده").grid_columnconfigure((0), weight=1)
    ################################################################################
    search_frame = CTkFrame(tab_view.tab("تعمیر درحال"))
    search_frame.grid(row=0, column=0,padx=20,sticky=E)
    search_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
    search_frame.grid_rowconfigure(0,weight=1)
    search_lbl = CTkLabel(search_frame,font=font,text="براساس شماره موبایل/کدملی")
    search_lbl.grid(row=0, column=3,padx=20,sticky=E)
    search_entry = CTkEntry(search_frame,140,35,placeholder_text='شماره موبایل/کدملی',justify=RIGHT)
    search_entry.grid(row=0, column=2,padx=20,sticky=E)
    search_btn = CTkButton(search_frame,text="جستوجو",font=font,command=search)
    search_btn.grid(row=0, column=1,padx=20,sticky=E)
    ##########################################################################
    search_frame_2 = CTkFrame(tab_view.tab("سفارش همه"))
    search_frame_2.grid(row=0, column=0,padx=20,sticky=E)
    search_frame_2.grid_columnconfigure((0, 1, 2, 3), weight=1)
    search_frame_2.grid_rowconfigure(0,weight=1)
    search_lbl_2 = CTkLabel(search_frame_2,font=font,text="براساس شماره موبایل/کدملی")
    search_lbl_2.grid(row=0, column=3,padx=20,sticky=E)
    search_entry_2 = CTkEntry(search_frame_2,140,35,placeholder_text='شماره موبایل/کدملی',justify=RIGHT)
    search_entry_2.grid(row=0, column=2,padx=20,sticky=E)
    search_btn_2 = CTkButton(search_frame_2,text="جستوجو",font=font,command=search_2)
    search_btn_2.grid(row=0, column=1,padx=20,sticky=E)
    ################################################################################
    search_frame_3 = CTkFrame(tab_view.tab("تحویل آماده"))
    search_frame_3.grid(row=0, column=0,padx=20,sticky=E)
    search_frame_3.grid_columnconfigure((0, 1, 2, 3), weight=1)
    search_frame_3.grid_rowconfigure(0,weight=1)
    search_lbl_3 = CTkLabel(search_frame_3,font=font,text="براساس شماره موبایل/کدملی")
    search_lbl_3.grid(row=0, column=3,padx=20,sticky=E)
    search_entry_3 = CTkEntry(search_frame_3,140,35,placeholder_text='شماره موبایل/کدملی',justify=RIGHT)
    search_entry_3.grid(row=0, column=2,padx=20,sticky=E)
    search_btn_3 = CTkButton(search_frame_3,text="جستوجو",font=font,command=search_3)
    search_btn_3.grid(row=0, column=1,padx=20,sticky=E)
    #############################################################################################
    sct = CTkScrollableFrame(tab_view.tab("تعمیر درحال"),200,200,0,5)
    sct.grid(row=1, column=0,rowspan=4,padx=20,sticky=NSEW)
    sct_2 = CTkScrollableFrame(tab_view.tab("سفارش همه"),200,200,0,5)
    sct_2.grid(row=1, column=0,rowspan=4,padx=20,sticky=NSEW)
    sct_3 = CTkScrollableFrame(tab_view.tab("تحویل آماده"),200,200,0,5)
    sct_3.grid(row=1, column=0,rowspan=4,padx=20,sticky=NSEW)
    sel_(),sel_2(),sel_3()

###########################################################################################
def show(data):
    clear_frame()
    try:
        conn = sqlite3.connect('pz.db')
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM paziresh")
        result = cursor.fetchone()
        b = result[0] + 1 if result[0] is not None else 1
        b+=1590
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while getting the next ID: {e}")
    
    
    def save_data():
        
        try:
            arrival = ent_date_of_arrival.get()
            departure = ent_departure_date.get()
            system = ent_input_system.get()
            system_type = combo_input_system_type.get()
            system_model = ent_input_system_model.get()
            try:
                system_serial = str(ent_input_system_serial.get())
            except ValueError:
                return messagebox.showerror("Error", "Serial number must be an integer.")
            input_name = ent_input_name.get()
            tel = ent_input_name_tel.get()
            code_meli = ent_input_name_code_meli.get()
            tel_sabet = ent_input_name_tel_sabet.get()
            adress = ent_input_name_adress.get("1.0", END).strip() #Get text from textbox
            problem = ent_problem.get("1.0", END).strip()
            try:
                cost = float(ent_cost.get())
            except ValueError:
                return messagebox.showerror("Error", "Cost must be a number.")
            description = ent_input_description.get("1.0", END).strip() #Get text from textbox
            Warrantyy = chek.get() 
            Warrantyy_mod = ent_modat_garanti.get()
            op_tek = ent_tak.get(0.0,END)
            status = chek_exit.get()
            if not all([system, system_type, system_model, input_name, tel, code_meli]):
                return messagebox.showerror("Error", "Please fill in all required fields.")
            if not validate_phone(tel):
                return messagebox.showerror("Error","Invalid phone number.")
            if not validate_code_meli(code_meli):
                return messagebox.showerror("Error","Invalid code meli.")

            data_tuple = (arrival, departure, system, system_type, system_model, system_serial, input_name, tel, code_meli, tel_sabet, adress, problem, cost, description,Warrantyy,Warrantyy_mod,op_tek,status)
            result = update_data(data,data_tuple)
            if isinstance(result, bool) and result: #Check if insert_data returned True(success)
                messagebox.showinfo("Success", "Data saved successfully!")
            else:
                messagebox.showerror("Error", result) #Show specific error message
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        tarikh_()
        
    def save_data_print():
        
        try:
            arrival = ent_date_of_arrival.get()
            departure = ent_departure_date.get()
            system = ent_input_system.get()
            system_type = combo_input_system_type.get()
            system_model = ent_input_system_model.get()
            try:
                system_serial = str(ent_input_system_serial.get())
            except ValueError:
                return messagebox.showerror("Error", "Serial number must be an integer.")
            input_name = ent_input_name.get()
            tel = ent_input_name_tel.get()
            code_meli = ent_input_name_code_meli.get()
            tel_sabet = ent_input_name_tel_sabet.get()
            adress = ent_input_name_adress.get("1.0", END).strip() #Get text from textbox
            problem = ent_problem.get("1.0", END).strip()
            try:
                cost = float(ent_cost.get())
            except ValueError:
                return messagebox.showerror("Error", "Cost must be a number.")
            description = ent_input_description.get("1.0", END).strip() #Get text from textbox
            Warrantyy = chek.get() 
            Warrantyy_mod = ent_modat_garanti.get()
            op_tek = ent_tak.get(0.0,END)
            status = chek_exit.get()
            if not all([system, system_type, system_model, input_name, tel, code_meli]):
                return messagebox.showerror("Error", "Please fill in all required fields.")
            if not validate_phone(tel):
                return messagebox.showerror("Error","Invalid phone number.")
            if not validate_code_meli(code_meli):
                return messagebox.showerror("Error","Invalid code meli.")

            data_tuple = (arrival, departure, system, system_type, system_model, system_serial, input_name, tel, code_meli, tel_sabet, adress, problem, cost, description,Warrantyy,Warrantyy_mod,op_tek,status)
            result = update_data(data,data_tuple)
            if isinstance(result, bool) and result: #Check if insert_data returned True(success)
                messagebox.showinfo("Success", "Data saved successfully!")
                curr_time = time.strftime("%H:%M:%S", time.localtime())
                context = {
                    'id':ent_input_id.get(),
                'garanti':chek.get(),
                'tarikh':ent_date_of_arrival.get(),
                'date':curr_time,
                'name_input':ent_input_name.get(),
                'system_name':ent_input_system.get(),
                'typee':combo_input_system_type.get(),
                'model':ent_input_system_model.get(),
                'seriyal':ent_input_system_serial.get(),
                'tel':ent_input_name_tel.get(),
                'addres':ent_input_name_adress.get("1.0", END),
                'moshkel':ent_input_description.get("1.0", END),
                'modat' : ent_modat_garanti.get()
                }
                temp_loder = jinja2.FileSystemLoader('./template/')
                temp_env = jinja2.Environment(loader=temp_loder)
                temp = temp_env.get_template('atar.html')
                output_text = temp.render(context)
                # Replace with your path
                config = pdfkit.configuration(wkhtmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
                pdfkit.from_string(output_text,f'./print_agin/sefaresh_{ent_input_id.get()}_mojadad.pdf',options={"encoding":'UTF-8','page-width': 210,'page-height': 151},configuration=config,)
                messagebox.showinfo("چاپ",'رسید پرینت شد')
            else:
                messagebox.showerror("Error", result) #Show specific error message
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        tarikh_()
        
    
    
    
    con = sqlite3.connect("pz.db")
    c = con.cursor()
    for i in c.execute(f'SELECT * FROM paziresh WHERE id={data}'):
        f_show = CTkFrame(root)
        f_show.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
        f_show.grid_columnconfigure((0,1,2,3,4,5), weight=1)
        f_show.grid_rowconfigure((0, 1, 2, 3), weight=1)
        f_show.grid_rowconfigure((4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,), weight=1)
        bt_back = customtkinter.CTkButton(f_show, text="بازگشت",font=font, fg_color= '#EA0000', hover_color = '#B20000', command=dashbord)
        bt_back.grid(row=13, column=0, padx=20, pady=(10, 0),sticky=E)

        bt_save = customtkinter.CTkButton(f_show, text="ذخیره",font=font,fg_color="green",hover_color="#00ff00",command=save_data)
        bt_save.grid(row=13, column=1, padx=20, pady=(10, 0),)
        
        bt_save = customtkinter.CTkButton(f_show, text="ذخیره و پرینت",font=font,fg_color="green",hover_color="#00ff00",command=save_data_print)
        bt_save.grid(row=13, column=2, padx=20, pady=(10, 0),sticky=W)
        
        lbl_id = CTkLabel(f_show, font=font,text=": شماره پذریش ")
        lbl_id.grid(row=0, column=5,pady=5)
        lbl_1 = CTkLabel(f_show, text="مشخصات دستگاه",font=font,corner_radius=20)
        lbl_1.grid(row=1,column=5,sticky=E,padx=10,pady=5)
        ent_input_id = CTkEntry(f_show,font=font_enry,justify=RIGHT)
        ent_input_id.grid(row=0, column=4)
        a = i[0]+1590
        ent_input_id.insert(0,a)
        ent_input_id.configure(state=DISABLED)
        
        lbl_date_of_arrival = CTkLabel(f_show, font=font,text=" : تاریخ ورود")
        lbl_date_of_arrival.grid(row=0, column=3,pady=5)
        ent_date_of_arrival = CTkEntry(f_show,font=font_enry,justify=RIGHT)
        ent_date_of_arrival.grid(row=0, column=2,pady=5)
        ent_date_of_arrival.insert(0,i[1])
        lbl_departure_date = CTkLabel(f_show, font=font,text=" : تاریخ خروج")
        lbl_departure_date.grid(row=0, column=1,pady=5)
        
        
        ent_departure_date = CTkEntry(f_show,font=font_enry)
        ent_departure_date.grid(row=0, column=0,pady=5)
        #########################################################################################
        frame_top = CTkFrame(f_show)
        frame_top.grid(row=2,column=0,columnspan=6,rowspan=3,sticky=NSEW) 
        frame_top.grid_columnconfigure((0,1,2,3,4,5),weight=1)
        frame_top.grid_rowconfigure((0,1),weight=1)
        lbl_input_system = CTkLabel(frame_top,text=" : نام دستگاه",font=font)
        lbl_input_system.grid(row=0,column=5)
        ent_input_system = CTkEntry(frame_top,font=font,justify=RIGHT)
        ent_input_system.insert(0,i[3])
        ent_input_system.grid(row=0,column=4)
        lbl_input_system_type = CTkLabel(frame_top,text=" : نوع دستگاه",font=font)
        lbl_input_system_type.grid(row=0,column=3)
        tv_list = [i[4]]
        if "LCD" in tv_list:
            tvs_list = ["LCD","LED","PLOSMA"]
        elif "LED" in tv_list:
            tvs_list = ["LED","LCD","PLOSMA"]
        else:
            tvs_list = ["PLOSMA","LED","LCD",]
        combo_input_system_type = CTkComboBox(frame_top,font=font_enry,values=tvs_list)
        combo_input_system_type.grid(row=0,column=2)
        lbl_input_system_model = CTkLabel(frame_top,text=" : مدل دستگاه",font=font)
        lbl_input_system_model.grid(row=0,column=1)
        ent_input_system_model = CTkEntry(frame_top,font=font,justify=RIGHT)
        ent_input_system_model.insert(0,i[5])
        ent_input_system_model.grid(row=0,column=0)
        lbl_input_system_serial = CTkLabel(frame_top,text=" : سریال دستگاه",font=font)
        lbl_input_system_serial.grid(row=1,column=5)
        ent_input_system_serial = CTkEntry(frame_top,font=font,justify=RIGHT)
        ent_input_system_serial.insert(0,i[6])
        ent_input_system_serial.grid(row=1,column=4)
        #########################################################################
        lbl_2 = CTkLabel(f_show, text="مشخصات مالک",font=font)
        lbl_2.grid(row=5,column=5,sticky=E,padx=10)
        frame_down = CTkFrame(f_show,)
        frame_down.grid(row=6,column=0,columnspan=6,rowspan=3,sticky=NSEW) 
        frame_down.grid_columnconfigure((0,1,2,3,4,5),weight=1)
        frame_down.grid_rowconfigure((0,1),weight=1)
        lbl_input_name = CTkLabel(frame_down,text=" : نام مالک",font=font)
        lbl_input_name.grid(row=0,column=5)
        ent_input_name = CTkEntry(frame_down,font=font_enry,justify=RIGHT)
        ent_input_name.insert(0,i[7])
        ent_input_name.grid(row=0,column=4)
        lbl_input_name_tel = CTkLabel(frame_down,text=" : شماره تلفن",font=font)
        lbl_input_name_tel.grid(row=0,column=3)
        ent_input_name_tel = CTkEntry(frame_down,font=font_enry,justify=LEFT)
        ent_input_name_tel.insert(0,f"0{i[8]}")
        ent_input_name_tel.grid(row=0,column=2)
        lbl_input_name_code_meli = CTkLabel(frame_down,text=" : کد ملی ",font=font)
        lbl_input_name_code_meli.grid(row=0,column=1,sticky=W)
        ent_input_name_code_meli = CTkEntry(frame_down,font=font_enry,justify=LEFT)
        ent_input_name_code_meli.insert(0,f"0{i[9]}")
        ent_input_name_code_meli.grid(row=0,column=0,sticky=E)
        lbl_input_name_tel_sabet = CTkLabel(frame_down,text=" : تلفن ثابت",font=font)
        lbl_input_name_tel_sabet.grid(row=1,column=5)
        ent_input_name_tel_sabet = CTkEntry(frame_down,font=font_enry,justify=RIGHT)
        ent_input_name_tel_sabet.insert(0,i[10])
        ent_input_name_tel_sabet.grid(row=1,column=4)
        lbl_input_name_adress = CTkLabel(frame_down,text=" : آدرس ",font=font)
        lbl_input_name_adress.grid(row=1,column=2,sticky=W)
        ent_input_name_adress = CTkTextbox(frame_down,height=100,font=font,corner_radius=10,width=400,border_width=3)
        ent_input_name_adress.tag_config("rtl",justify=RIGHT)
        ent_input_name_adress.tag_add("rtl",0.0,END)
        ent_input_name_adress.insert(0.0,i[11],'rtl')
        ent_input_name_adress.grid(row=1,column=0,columnspan=2,)
        #############################################################################
        lbl_3 = CTkLabel(f_show, text="مشخصات مشکل",font=font)
        lbl_3.grid(row=9,column=5,sticky=E,padx=10)
        frame_moshkel = CTkFrame(f_show)
        frame_moshkel.grid(row=10,column=0,columnspan=6,rowspan=3,sticky=NSEW) 
        frame_moshkel.grid_columnconfigure((0,1,2,3,4),weight=1)
        frame_moshkel.grid_rowconfigure((0,1,2),weight=1)
        lbl_problem = CTkLabel(frame_moshkel,text=' : ایراد ظاهری',font=font)
        lbl_problem.grid(row=0,column=3,)
        ent_problem = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)
        ent_problem.grid(row=0,column=2,sticky=E)
        ent_problem.tag_config('rtl',justify=RIGHT)
        ent_problem.tag_add('rtl',0.0,END)
        ent_problem.insert(0.0,i[12],'rtl')
        lbl_cost = CTkLabel(frame_moshkel,text=' : هزینه ',font=font)
        lbl_cost.grid(row=0,column=1,sticky=E)
        ent_cost = CTkEntry(frame_moshkel,font=font_enry,justify=RIGHT)
        ent_cost.grid(row=0,column=0,sticky=E)
        ent_cost.insert(0,i[13])
        lbl_input_description = CTkLabel(frame_moshkel,text=" : توضیحات ",font=font)
        lbl_input_description.grid(row=1,column=3)
        ent_input_description = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)
        ent_input_description.tag_config("rtl",justify=RIGHT)
        ent_input_description.tag_add("rtl",0.0,END)
        ent_input_description.insert(0.0,i[14],'rtl')
        ent_input_description.grid(row=1,column=2,sticky=E)
        lbl_tak = CTkLabel(frame_moshkel,text=": نظر تکنسین",font=font)
        lbl_tak.grid(row=2,column=3)
        ent_tak = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)
        ent_tak.tag_config("rtl",justify=RIGHT)
        ent_tak.tag_add("rtl",0.0,END)
        ent_tak.insert(0.0,i[17],'rtl')
        ent_tak.grid(row=2,column=2,sticky=E,)
        lbl_chek = CTkLabel(frame_moshkel,0,28,font=font,text="آیاگارانتی دارد؟")
        lbl_chek.grid(row=1,column=1,sticky=E)
        lbl_modat_garanti =CTkLabel(frame_moshkel,font=font,text="مدت گارنتی",)
        lbl_modat_garanti.grid(row=2,column=1,sticky=NE,)
        ent_modat_garanti =CTkEntry(frame_moshkel,placeholder_text="مدت گارانتی",font=font_enry,justify=CENTER,)
        
        ent_modat_garanti.insert(0,i[16])
        ent_modat_garanti.grid(row=2,column=1,sticky=E,)
        def modat():
            if chek.get() == "بلی":
                ent_modat_garanti.configure(state=NORMAL)
            elif chek.get() == "خیر":
                ent_modat_garanti.configure(state=DISABLED)
        def exittt():
            if chek_exit.get() == 1:
                ent_departure_date.insert(0,JalaliDate.today().strftime('%Y/%m/%d'))
                ent_departure_date.configure(state=DISABLED)
        b = int(i[18])
        val = IntVar(value=b)
        chek_exit = CTkCheckBox(frame_moshkel,text="آماده تحویل",font=font,onvalue=1,variable=val,offvalue=0,command=exittt)
        chek_exit.grid(row=2,column=0,sticky=E)
        
        abbbb = f'{i[15]}'
        str_ = StringVar(value=abbbb)
        chek = CTkCheckBox(frame_moshkel,30,text="بلی",font=font,onvalue="بلی",offvalue="خیر",variable=str_,command=modat)
        chek.grid(row=1,column=0,sticky=E)
        chek_2 = CTkCheckBox(frame_moshkel,text="خیر",font=font,onvalue="خیر",offvalue="بلی",variable=str_,command=modat)
        chek_2.grid(row=1,column=0,)
        def exitt():
            if chek_exit.get() == 1:
                ent_departure_date.insert(0,JalaliDate.today().strftime('%Y/%m/%d'))
                ent_departure_date.configure(state=DISABLED)
        exitt()

def login():
    far = CTkFrame(root)
    far.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far.grid_columnconfigure((0,1,2,), weight=1)
    # far.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
    far.grid_rowconfigure(( 0, 1, 2, 3, 4, 5, 6, ), weight=1)
    btn_quit = customtkinter.CTkButton(far, text="خروج", fg_color= '#EA0000', hover_color = '#B20000',font=font, command= close_window)
    btn_quit.grid(row=5, column=1, padx=20, pady=0)
    
    lbl_user = CTkLabel(far,0,28,text='ورود به سیستم',font=CTkFont(family="Vazir",size=50,weight='bold'))
    lbl_user.grid(row=1,column=1,padx=20,sticky=S)
    def create_table_admin():
        conn = sqlite3.connect('pz.db')
        cursor = conn.cursor()
        conn.execute('''create table if not exists ADMIN
                    (name_id INTEGER PRIMARY KEY,
                    USER varchar(20) NOT NULL,
                    PASSWORD varchar(20) NOT NULL)''')
        admin = [('admin', '7070816')]
        cursor.execute("SELECT MAX(name_id) FROM ADMIN")
        result = cursor.fetchone()
        if result[0] == 1:
            pass
        else:
            conn.executemany('INSERT INTO ADMIN(USER, PASSWORD) VALUES (?,?)', admin)
        conn.commit()
        conn.close()
    
    def login_admin():
        conn = sqlite3.connect('pz.db')
        cursor = conn.cursor()
        for i in conn.execute('SELECT * FROM ADMIN'):
            user = i[1]
            password = i[2]
        conn.commit()
        conn.close()
        if user == ent_user_login.get() and password == ent_password_login.get():
            dashbord()
            return messagebox.showinfo("ورود به سیستم", ".با موفقیت وارد شدید")
        else:
            return messagebox.showerror("مشکل", ".نام کاربری/رمز عبور نادرست است")
    create_table_admin()
    
        
    
    fram_login = CTkFrame(far,500,350,3,10,border_color='blue')
    fram_login.grid(row=2,column=1,rowspan=2,ipady=50,ipadx=50)
    fram_login.grid_columnconfigure((0,1,), weight=1)
    fram_login.grid_rowconfigure(( 0, 1,), weight=1)
    CTkLabel(fram_login,text=': نام کاربری',font=font).grid(row=0,column=1) 
    ent_user_login = CTkEntry(fram_login,font=font_enry,justify=RIGHT,width=200,placeholder_text='نام کاربری')
    ent_user_login.grid(row=0,column=0,columnspan=1,)
    CTkLabel(fram_login,text=': رمز عبور',font=font).grid(row=1,column=1) 
    ent_password_login = CTkEntry(fram_login,font=font_enry,justify=RIGHT,width=200,placeholder_text='رمز عبور',show="*")
    ent_password_login.grid(row=1,column=0,columnspan=1,)
    btn_login = customtkinter.CTkButton(far, text="ورود", fg_color="green", hover_color="#009933",font=font, command= login_admin)
    btn_login.grid(row=4, column=1, padx=20, pady=0)
    
    
# login()
# paziresh_()
# tarikh_()
dashbord()
# show(1)
# send_sms()

root.mainloop()