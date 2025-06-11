from project23 import *
from db_pz import create_database,db_tel,create_settings_table,save_sender_number, get_sender_number
from ines_data import insert_data,update_data,insert_tel
from create_dictory import create_dictory
import tarikheh as Tarikh 
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

create_dictory()
create_database()
db_tel()
create_settings_table()
current_user = None



def validate_phone(phone_number):
  #Basic phone number validation (adjust regex as needed)
  pattern = r"^\+?\d{11}$" #Example: Accepts numbers starting with optional +, min 10 digits
  return bool(re.match(pattern, phone_number))


def del_data(id_):
    a = messagebox.askquestion('سوال','آیا از حذف مطمعن هستید')
    if a == 'yes' :
        try:
            conn = sqlite3.connect('database/pz.db')
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM paziresh WHERE id={id_}")
            conn.commit()
            conn.close()
            tarikh_()
            return True
        except sqlite3.Error as e: # More informative error message
            tarikh_()
            return False
    else:
        tarikh_()

def validate_code_meli(code_meli):
  #Basic code meli validation (Adjust if needed)
  pattern = r"^\d{10}$" # Example: 10 digits
  return bool(re.match(pattern, code_meli))





DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("dark-blue")


root = CTk()
root.iconbitmap('icon/tv.ico')
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure((0, 1, 2, 3), weight=0)
root.grid_rowconfigure((4, 5, 6, 7), weight=1)
# root.overrideredirect(True)
root.title('Behroz Electronic')
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
api = KavenegarAPI("742F364166354D7762516C617272357A545936513567685A5064344851557141504D726D65645A337132493D")
font = CTkFont(family="Vazir",size=25,weight='bold')
font_enry=CTkFont(family="Vazir",size=20)

###################################################################################### SMS

def taki(number, message):
    try:
        sender = get_sender_number()
        params = {
            'receptor': number,
            'sender': sender,
            'message': message,
        }
        response = api.sms_send(params)
    except APIException as e:
        return messagebox.showerror("خطا", f"Error: {e}")
    except Exception as e:
        dashbord()
        return messagebox.showinfo('خطا', f"Unexpected error: {e}")

def koli(numbers, message):
    try:
        sender = get_sender_number()
        params = {
            'receptor': numbers,
            'sender': sender,
            'message': message,
        }
        response = api.sms_send(params)
    except APIException as e:
        return messagebox.showerror("خطا", f"Error: {e}")
    except Exception as e:
        dashbord()
        return messagebox.showinfo('خطا', f"Unexpected error: {e}")


def save_numbers_to_db(numbers: list[str]):
    con = sqlite3.connect("database/pz.db")
    c = con.cursor()
    
    for num in numbers:
        num = num.strip()
        if re.fullmatch(r"\d{11}", num):  # فقط 11 رقم عددی
            exists = c.execute("SELECT 1 FROM PHONE WHERE tel = ?", (num,)).fetchone()
            if not exists:
                c.execute("INSERT INTO PHONE (tel) VALUES (?)", (num,))
    
    con.commit()
    con.close()

def handle_save_only(numbers_text: str):
    numbers = [tel.strip() for tel in numbers_text.splitlines() if tel.strip()]
    valid_numbers = [num for num in numbers if re.fullmatch(r"\d{11}", num)]

    if valid_numbers:
        save_numbers_to_db(valid_numbers)
        messagebox.showinfo("موفقیت", "شماره‌های معتبر با موفقیت ذخیره شدند.")
    else:
        messagebox.showwarning("هشدار", "هیچ شماره‌ی ۱۱ رقمی معتبری وارد نشده است.")

def load_numbers_from_file(textbox):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                numbers = f.read()
                textbox.delete("0.0", END)
                textbox.insert("0.0", numbers)
        except Exception as e:
            messagebox.showerror("خطا", f"خطا در خواندن فایل: {e}")


###################################################################################### SMS

########################################################################################## admin 


def save_new_user(username, password):
    hashed_pass = hash_password(password)
    try:
        conn = sqlite3.connect('database/pz.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ADMIN(USER, PASSWORD) VALUES (?, ?)", (username, hashed_pass))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # نام کاربری قبلا ثبت شده است
        return False

def update_password(old_pass, new_pass, current_user):
    hashed_old = hash_password(old_pass)
    hashed_new = hash_password(new_pass)
    conn = sqlite3.connect('database/pz.db')
    cursor = conn.cursor()
    cursor.execute("SELECT PASSWORD FROM ADMIN WHERE USER=?", (current_user,))
    result = cursor.fetchone()
    if result and result[0] == hashed_old:
        cursor.execute("UPDATE ADMIN SET PASSWORD=? WHERE USER=?", (hashed_new, current_user))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

########################################################################################## admin 

def clear_frame():
  for widget in root.winfo_children():
    widget.destroy()
    

def close_window(): 
    root.destroy()
    
def dashbord():
    clear_frame()
    far = CTkFrame(root)
    far.grid(row=1, column=0, rowspan=7, sticky=NSEW)    
    far.grid_columnconfigure(0, weight=1)
    far.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6 ,7), weight=1)

    bt_dashboard = customtkinter.CTkButton(far, text="پذیرش", height=60, font=font,  command=paziresh_)
    bt_dashboard.grid(row=1, column=0, padx=20, pady=20)

    bt_sms = customtkinter.CTkButton(far, text="ارسال پیامک", height=60, font=font,  command=send_sms_ui)
    bt_sms.grid(row=2, column=0, padx=20, pady=20)

    bt_tarikh = customtkinter.CTkButton(far, text="تاریخچه", height=60, font=font,  command=tarikh_)
    bt_tarikh.grid(row=3, column=0, padx=20, pady=20)

    bt_settings = customtkinter.CTkButton(far, text="تنظیمات", height=60, font=font,  command=settings_ui)
    bt_settings.grid(row=4, column=0, padx=20, pady=20)
    
    bt_settings_sms = customtkinter.CTkButton(far, text="تنظیمات اس‌ام‌اس", height=60, font=font,  command=sms_settings_ui)
    bt_settings_sms.grid(row=5, column=0, padx=20, pady=20)

    btn_quit = customtkinter.CTkButton(far, text="خروج", height=60, fg_color="#C74949", hover_color='#B20000', font=font, command=close_window)
    btn_quit.grid(row=6, column=0, padx=20, pady=0)

def paziresh_():
    create_database()
    clear_frame()
    try:
        conn = sqlite3.connect('database/pz.db')
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
                'moshkel':ent_problem.get("1.0", END),
                'modat' : ent_modat_garanti.get()
                }
                temp_loder = jinja2.FileSystemLoader('./template/')
                temp_env = jinja2.Environment(loader=temp_loder)
                temp = temp_env.get_template('atar.html')
                output_text = temp.render(context)
                # Replace with your path
                config = pdfkit.configuration(wkhtmltopdf = "./wkhtmltopdf/bin/wkhtmltopdf.exe")
                pdfkit.from_string(output_text,f'./print/paziresh_{ent_input_id.get()}.pdf',options={"encoding":'UTF-8','page-width': 210,'page-height': 151},configuration=config,)
                messagebox.showinfo("چاپ",'رسید پرینت شد')
            else:
                messagebox.showerror("Error", result) #Show specific error message
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        dashbord()
        
            
        
        
    far_2 = CTkFrame(root,)
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
    frame_top = CTkFrame(far_2,)
    frame_top.grid(row=2,column=0,columnspan=6,rowspan=3,sticky=NSEW) 
    frame_top.grid_columnconfigure((0,1,2,3,4,5),weight=1)
    frame_top.grid_rowconfigure((0,1),weight=1)
    lbl_input_system = CTkLabel(frame_top,text=" : نام دستگاه",font=font)
    lbl_input_system.grid(row=0,column=5)
    ent_input_system = CTkEntry(frame_top,font=font,justify=RIGHT)
    ent_input_system.grid(row=0,column=4)
    lbl_input_system_type = CTkLabel(frame_top,text=" : نوع دستگاه",font=font)
    lbl_input_system_type.grid(row=0,column=3)
    tv_list = ['LED','LCD','PLOSMA']
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

    ent_input_name_adress.grid(row=1,column=0,columnspan=2)
    #############################################################################
    lbl_3 = CTkLabel(far_2, text="مشخصات مشکل",font=font)
    lbl_3.grid(row=9,column=5,sticky=E,padx=10)
    frame_moshkel = CTkFrame(far_2,)
    frame_moshkel.grid(row=10,column=0,columnspan=6,rowspan=3,sticky=NSEW) 
    frame_moshkel.grid_columnconfigure((0,1,2,3,4),weight=1)
    frame_moshkel.grid_rowconfigure((0,1,2),weight=1)
    lbl_problem = CTkLabel(frame_moshkel,text=' : ایراد ظاهری',font=font)
    lbl_problem.grid(row=0,column=3,)
    ent_problem = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)
    ent_problem.grid(row=0,column=2,sticky=E)
    lbl_cost = CTkLabel(frame_moshkel,text=' : هزینه ',font=font)
    lbl_cost.grid(row=0,column=1,sticky=E)
    ent_cost = CTkEntry(frame_moshkel,font=font_enry,justify=RIGHT)
    ent_cost.grid(row=0,column=0,sticky=E)
    ent_cost.insert(0,0)
    lbl_input_description = CTkLabel(frame_moshkel,text=" : توضیحات ",font=font)
    lbl_input_description.grid(row=1,column=3)
    ent_input_description = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)

    ent_input_description.grid(row=1,column=2,sticky=E)
    lbl_tak = CTkLabel(frame_moshkel,text=": نظر تکنسین",font=font)
    lbl_tak.grid(row=2,column=3)
    ent_tak = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)


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
    chek_2 = CTkCheckBox(frame_moshkel,30,text="خیر",font=font,onvalue="خیر",offvalue="بلی",variable=str_,command=modat)
    chek_2.grid(row=1,column=0,)
    
def send_sms_ui():
    con = sqlite3.connect("database/pz.db")
    c = con.cursor()

    tel_dakheli = [f'0{int(t[0])}' for t in c.execute('SELECT tel FROM paziresh')]
    tel_afzode = [f'0{int(t[0])}' for t in c.execute('SELECT tel FROM PHONE')]
    con.close()
    tel_all = tel_dakheli + tel_afzode

    parent_frame = CTkFrame(root, )
    parent_frame.grid(row=1, column=0, rowspan=7, sticky=NSEW)
    parent_frame.grid_columnconfigure(0, weight=1)
    parent_frame.grid_rowconfigure((1,2,3,4,5,6,7), weight=1)

    # متن پیام ورودی
    lbl_msg = CTkLabel(parent_frame, text='متن پیام:', font=font)
    lbl_msg.grid(row=0, column=0, pady=5, padx=10)
    txt_msg = CTkTextbox(parent_frame, height=200, font=font_enry, width=600)
    txt_msg.grid(row=1, column=0, padx=20, pady=10)

    # تب‌ها
    tabs = CTkTabview(parent_frame, width=600)
    tabs.grid(row=2, column=0, padx=20, pady=10)
    tabs.add("ارسال تکی")
    tabs.add("دستگاه داخل")
    tabs.add("شده افزوده")
    tabs.add("همه شماره‌ها")
    tabs.add("افزودن دستی / از فایل")

    # تب ارسال تکی
    CTkLabel(tabs.tab("ارسال تکی"), text="شماره موبایل (یا چندتا با کاما جدا کنید):", font=font).pack(pady=5)
    entry_single = CTkEntry(tabs.tab("ارسال تکی"), font=font_enry, width=400)
    entry_single.pack(pady=5)
    CTkButton(
        tabs.tab("ارسال تکی"),
        text="ارسال",
        font=font,
        command=lambda: taki(entry_single.get(), txt_msg.get("0.0", END).strip())
    ).pack(pady=10)

    # تب دستگاه داخل
    sc1 = CTkScrollableFrame(tabs.tab("دستگاه داخل"), height=200)
    sc1.pack(pady=5)
    for tel in tel_dakheli:
        e = CTkEntry(sc1, font=font_enry, width=400)
        e.insert(END, tel)
        e.configure(state="disabled")
        e.pack(padx=10, pady=2)
    CTkButton(
        tabs.tab("دستگاه داخل"),
        text="ارسال گروهی",
        font=font,
        command=lambda: koli(tel_dakheli, txt_msg.get("0.0", END).strip())
    ).pack(pady=10)

    # تب شده افزوده
    sc2 = CTkScrollableFrame(tabs.tab("شده افزوده"), height=200)
    sc2.pack(pady=5)
    for tel in tel_afzode:
        e = CTkEntry(sc2, font=font_enry, width=400)
        e.insert(END, tel)
        e.configure(state="disabled")
        e.pack(padx=10, pady=2)
    CTkButton(
        tabs.tab("شده افزوده"),
        text="ارسال گروهی",
        font=font,
        command=lambda: koli(tel_afzode, txt_msg.get("0.0", END).strip())
    ).pack(pady=10)

    # تب همه شماره‌ها
    sc3 = CTkScrollableFrame(tabs.tab("همه شماره‌ها"), height=200)
    sc3.pack(pady=5)
    for tel in tel_all:
        e = CTkEntry(sc3, font=font_enry, width=400)
        e.insert(END, tel)
        e.configure(state="disabled")
        e.pack(padx=10, pady=2)
    CTkButton(
        tabs.tab("همه شماره‌ها"),
        text="ارسال گروهی",
        font=font,
        command=lambda: koli(tel_all, txt_msg.get("0.0", END).strip())
    ).pack(pady=10)

    # تب افزودن دستی / فایل
    manual_entry = CTkTextbox(tabs.tab("افزودن دستی / از فایل"), height=150, width=550, font=font_enry)
    manual_entry.pack(pady=5)
    CTkButton(
        tabs.tab("افزودن دستی / از فایل"),
        text="بارگذاری شماره‌ها از فایل",
        font=font,
        command=lambda: load_numbers_from_file(manual_entry)
    ).pack(pady=5)
    CTkButton(
        tabs.tab("افزودن دستی / از فایل"),
        text="ذخیره",
        font=font,
        command=lambda: handle_save_only(manual_entry.get("0.0", END))
    ).pack(pady=10)


    # دکمه بازگشت
    CTkButton(parent_frame, text="بازگشت", fg_color="#C74949", hover_color='#B20000', font=font, command=dashbord).grid(row=5, column=0, pady=(5, 10))

def settings_ui():
    clear_frame()
    frame_settings = CTkFrame(root, )
    frame_settings.grid(row=1, column=0, rowspan=7, sticky=NSEW)
    frame_settings.grid_columnconfigure(0, weight=1)
    frame_settings.grid_rowconfigure(tuple(range(13)), weight=1)

    # --- عنوان اصلی ---
    CTkLabel(frame_settings, text="تنظیمات", font=CTkFont(family="Vazir", size=36, weight="bold"),
             text_color="#333").grid(row=0, column=0, pady=10)

    # --- فقط admin مجاز به تعریف کاربر جدید ---
    if current_user == "admin":
        CTkLabel(frame_settings, text="تعریف کاربر جدید", font=font, text_color="#222").grid(row=1, column=0, pady=(5, 0))

        entry_username = CTkEntry(frame_settings, placeholder_text="نام کاربری")
        entry_username.grid(row=2, column=0, padx=20, pady=5)

        entry_password = CTkEntry(frame_settings, placeholder_text="رمز عبور", show="*")
        entry_password.grid(row=3, column=0, padx=20, pady=5)

        lbl_user_result = CTkLabel(frame_settings, text="", text_color="green")
        lbl_user_result.grid(row=4, column=0, pady=5)

        def add_user():
            username = entry_username.get()
            password = entry_password.get()
            if username and password:
                save_new_user(username, password)
                lbl_user_result.configure(text="✅ کاربر جدید ثبت شد.", text_color="green")
                entry_username.delete(0, "end")
                entry_password.delete(0, "end")
            else:
                lbl_user_result.configure(text="⚠ لطفاً نام کاربری و رمز عبور را وارد کنید.", text_color="red")

        btn_add_user = CTkButton(frame_settings, text="ثبت کاربر جدید", command=add_user, fg_color="#0066cc", hover_color="#005bb5")
        btn_add_user.grid(row=5, column=0, pady=10)

    # --- بخش تغییر رمز عبور ---
    CTkLabel(frame_settings, text="تغییر رمز عبور", font=font, text_color="#222").grid(row=6, column=0, pady=(20, 5))

    entry_old_pass = CTkEntry(frame_settings, placeholder_text="رمز فعلی", show="*")
    entry_old_pass.grid(row=7, column=0, padx=20, pady=5)

    entry_new_pass = CTkEntry(frame_settings, placeholder_text="رمز جدید", show="*")
    entry_new_pass.grid(row=8, column=0, padx=20, pady=5)

    lbl_pass_result = CTkLabel(frame_settings, text="", text_color="red")
    lbl_pass_result.grid(row=9, column=0, pady=5)

    def change_password():
        old_pass = entry_old_pass.get()
        new_pass = entry_new_pass.get()

        global current_user
        if current_user is None:
            lbl_pass_result.configure(text="❌ کاربر شناسایی نشد!", text_color="red")
            return

        if old_pass and new_pass:
            result = update_password(old_pass, new_pass, current_user)
            if result:
                lbl_pass_result.configure(text="✅ رمز با موفقیت تغییر کرد.", text_color="green")
                entry_old_pass.delete(0, "end")
                entry_new_pass.delete(0, "end")
            else:
                lbl_pass_result.configure(text="❌ رمز فعلی اشتباه است.", text_color="red")
        else:
            lbl_pass_result.configure(text="⚠ لطفا هر دو فیلد را پر کنید.", text_color="red")

    btn_change_pass = CTkButton(frame_settings, text="تغییر رمز", command=change_password,
                                fg_color="#009933", hover_color="#007a29")
    btn_change_pass.grid(row=10, column=0, pady=10)

    # --- دکمه بازگشت به داشبورد ---
    btn_back = CTkButton(frame_settings, text="بازگشت", command=dashbord,
                         fg_color="#cc5050", hover_color="#D61010", text_color="black")
    btn_back.grid(row=11, column=0, pady=10)


def sms_settings_ui():
    clear_frame()
    frame_sms = CTkFrame(root,  corner_radius=20)
    frame_sms.grid(row=1, column=0, rowspan=7, sticky=NSEW)
    frame_sms.grid_columnconfigure(0, weight=1)
    frame_sms.grid_rowconfigure(tuple(range(6)), weight=1)

    # --- عنوان اصلی ---
    CTkLabel(
        frame_sms,
        text="تنظیم شماره ارسال پیامک",
        font=CTkFont(family="Vazir", size=32, weight="bold"),
        text_color="#222"
    ).grid(row=0, column=0, pady=(40, 20))

    # --- فیلد شماره ---
    sender_var = customtkinter.StringVar(value=get_sender_number())

    entry_sender = CTkEntry(
        frame_sms,
        textvariable=sender_var,
        placeholder_text="مثلاً: 200060006069",
        font=CTkFont(family="Vazir", size=20),
        height=50,
        width=300,
        corner_radius=12,
        border_width=2,
        border_color="#cccccc"
    )
    entry_sender.grid(row=1, column=0, padx=40, pady=10)

    # --- پیام وضعیت ---
    lbl_sms_status = CTkLabel(frame_sms, text="", text_color="green", font=font)
    lbl_sms_status.grid(row=2, column=0, pady=10)

    # --- دکمه ذخیره ---
    CTkButton(
        frame_sms,
        text="💾 ذخیره شماره",
        command=lambda: save_number(),
        fg_color="#00b894",
        hover_color="#019170",
        font=CTkFont(family="Vazir", size=18, weight="bold"),
        text_color="white",
        height=45,
        corner_radius=12
    ).grid(row=3, column=0, pady=20)

    # --- دکمه بازگشت ---
    CTkButton(
        frame_sms,
        text="⬅ بازگشت به داشبورد",
        command=dashbord,
        fg_color="#dfe6e9",
        hover_color="#b2bec3",
        font=CTkFont(family="Vazir", size=16),
        text_color="black",
        height=40,
        corner_radius=12
    ).grid(row=4, column=0, pady=10)

    # --- تابع ذخیره شماره ---
    def save_number():
        number = sender_var.get().strip()
        if number:
            save_sender_number(number)
            lbl_sms_status.configure(text="✅ شماره ذخیره شد.", text_color="green")
        else:
            lbl_sms_status.configure(text="⚠ لطفاً شماره را وارد کنید.", text_color="red")


def tarikh_():
    
    def run_search(entry_value, sct_frame, status=None):
        con = sqlite3.connect("database/pz.db")
        c = con.cursor()
        Tarikh.clear_frame(sct_frame)

        if len(entry_value) == 11:
            query = "SELECT * FROM paziresh WHERE tel=?"
            params = [entry_value]
        elif len(entry_value) == 10:
            query = "SELECT * FROM paziresh WHERE code_meli=?"
            params = [entry_value]
        elif entry_value == "":
            return None
        else:
            return "invalid"

        # اگر وضعیت مشخص شده
        if status is not None:
            if isinstance(status, list):
                placeholders = ",".join("?" for _ in status)
                query += f" AND status IN ({placeholders})"
                params.extend(status)
            else:
                query += " AND status=?"
                params.append(status)

        for row in c.execute(query, params):
            a = row[0] + 1590
            s = CTkFrame(sct_frame, border_width=3, fg_color='blue')
            s.pack(pady=3, anchor=E)
            s.grid_columnconfigure([0, 1], weight=1)
            s.grid_rowconfigure([0], weight=1)
            ent_id = CTkLabel(s,63,28,text=a,font=font_enry,text_color="black",fg_color="#d9d9d9",corner_radius=5,anchor=CENTER)

            ent_id.grid(row=0, column=10, sticky=E)
            Tarikh.create_data_row(s, font_enry, font, row, 0, show, del_data)

        con.commit()
        con.close()
        return "ok"
  
    def search():
        result = run_search(search_entry.get(), sct, status=0)
        if result == "invalid":
            sel_()
            return messagebox.showerror("مشکل", ".شماره موبایل/کدملی اشتباه است")
        elif result is None:
            sel_()
        
    def search_2():
        result = run_search(search_entry_2.get(), sct_2, status=[0,1])
        if result == "invalid":
            sel_2()
            return messagebox.showerror("مشکل", ".شماره موبایل/کدملی اشتباه است")
        elif result is None:
            sel_2()

    def search_3():
        result = run_search(search_entry_3.get(), sct_3, status=1)
        if result == "invalid":
            sel_3()
            return messagebox.showerror("مشکل", ".شماره موبایل/کدملی اشتباه است")
        elif result is None:
            sel_3()      
    
    def sel_():
        
        s = CTkFrame(sct,border_width=3)
        s.pack(pady=3,anchor=E)
        s.grid_columnconfigure([0,1],weight=1)
        s.grid_rowconfigure([0],weight=1)
        ent_id = CTkLabel(s,
            text='شماره پذیرش',
            font=CTkFont('Vazir',11),
            fg_color="#d9d9d9",         # رنگ پس‌زمینه شبیه CTkEntry غیرفعال
            text_color="black",         # رنگ متن
            corner_radius=5,            # گوشه‌های گرد
            width=63,
            height=28,
            anchor=CENTER )
        ent_id.grid(row=0,column=10,sticky=E)
        Tarikh.create_header(s,font_enry)  
        con = sqlite3.connect("database/pz.db")
        c = con.cursor()
        for row in c.execute('SELECT * FROM paziresh WHERE status=0 ORDER BY id DESC LIMIT 10').fetchall():
            a=row[0]+1590
            s = CTkFrame(sct,border_width=3,fg_color='blue')
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkLabel(s,63,28,text=a,font=font_enry,text_color="black",fg_color="#d9d9d9",corner_radius=5,anchor=CENTER)
            ent_id.grid(row=0,column=10,sticky=E)
            Tarikh.create_data_row(s, font_enry, font, row, 0, show, del_data)
        con.commit()
        con.close()
    
    def sel_2():
        s = CTkFrame(sct_2,border_width=3)
        s.pack(pady=3,anchor=E)
        s.grid_columnconfigure([0,1],weight=1)
        s.grid_rowconfigure([0],weight=1)
        ent_id = CTkLabel(s,
            text='شماره پذیرش',
            font=CTkFont('Vazir',11),
            fg_color="#d9d9d9",         # رنگ پس‌زمینه شبیه CTkEntry غیرفعال
            text_color="black",         # رنگ متن
            corner_radius=5,            # گوشه‌های گرد
            width=63,
            height=28,
            anchor=CENTER )
        ent_id.grid(row=0,column=10,sticky=E)
        Tarikh.create_header(s,font_enry)
        
        con = sqlite3.connect("database/pz.db")
        c = con.cursor()
        for row in c.execute('SELECT * FROM paziresh ORDER BY id DESC LIMIT 10').fetchall():
            a=row[0]+1590
            s = CTkFrame(sct_2,border_width=3,fg_color='blue')
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkLabel(s,63,28,text=a,font=font_enry,text_color="black",fg_color="#d9d9d9",corner_radius=5,anchor=CENTER)
            
            ent_id.grid(row=0,column=10,sticky=E)
            Tarikh.create_data_row(s, font_enry, font, row, 0, show, del_data)
        con.commit()
        con.close()
        
    def sel_3():
        s = CTkFrame(sct_3,border_width=3)
        s.pack(pady=3,anchor=E)
        s.grid_columnconfigure([0,1],weight=1)
        s.grid_rowconfigure([0],weight=1)
        ent_id = CTkLabel(s,
            text='شماره پذیرش',
            font=CTkFont('Vazir',11),
            fg_color="#d9d9d9",         # رنگ پس‌زمینه شبیه CTkEntry غیرفعال
            text_color="black",         # رنگ متن
            corner_radius=5,            # گوشه‌های گرد
            width=63,
            height=28,
            anchor=CENTER )
        ent_id.grid(row=0,column=10,sticky=E)
        Tarikh.create_header(s,font_enry)
        con = sqlite3.connect("database/pz.db")
        c = con.cursor()
        for row in c.execute('SELECT * FROM paziresh WHERE status=1 ORDER BY id DESC LIMIT 10').fetchall():
            a=row[0]+1590
            s = CTkFrame(sct_3,border_width=3,fg_color='blue')
            s.pack(pady=3,anchor=E)
            s.grid_columnconfigure([0,1],weight=1)
            s.grid_rowconfigure([0],weight=1)
            ent_id = CTkLabel(s,63,28,text=a,font=font_enry,text_color="black",fg_color="#d9d9d9",corner_radius=5,anchor=CENTER)
            ent_id.grid(row=0,column=10,sticky=E)
            Tarikh.create_data_row(s, font_enry, font, row, 0, show, del_data)
        con.commit()
        con.close()
    
    far_4 = CTkFrame(root,)
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
    search_frame = CTkFrame(tab_view.tab("تعمیر درحال"),)
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
    search_frame_2 = CTkFrame(tab_view.tab("سفارش همه"),)
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
    search_frame_3 = CTkFrame(tab_view.tab("تحویل آماده"),)
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
        conn = sqlite3.connect('database/pz.db')
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
                'moshkel':ent_problem.get("1.0", END),
                'modat' : ent_modat_garanti.get()
                }
                temp_loder = jinja2.FileSystemLoader('./template/')
                temp_env = jinja2.Environment(loader=temp_loder)
                temp = temp_env.get_template('atar.html')
                output_text = temp.render(context)
                # Replace with your path
                config = pdfkit.configuration(wkhtmltopdf = "./wkhtmltopdf/bin/wkhtmltopdf.exe")
                pdfkit.from_string(output_text,f'./print_agin/paziresh_{ent_input_id.get()}_mojadad.pdf',options={"encoding":'UTF-8','page-width': 210,'page-height': 151},configuration=config,)
                messagebox.showinfo("چاپ",'رسید پرینت شد')
            else:
                messagebox.showerror("Error", result) #Show specific error message
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        tarikh_()
        
    
    
    
    con = sqlite3.connect("database/pz.db")
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
        ent_departure_date.insert(0,i[2])
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
        ent_input_name_adress.insert(0.0,i[11])
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
        ent_problem.insert(0.0,i[12])
        lbl_cost = CTkLabel(frame_moshkel,text=' : هزینه ',font=font)
        lbl_cost.grid(row=0,column=1,sticky=E)
        ent_cost = CTkEntry(frame_moshkel,font=font_enry,justify=RIGHT)
        ent_cost.grid(row=0,column=0,sticky=E)
        ent_cost.insert(0,i[13])
        lbl_input_description = CTkLabel(frame_moshkel,text=" : توضیحات ",font=font)
        lbl_input_description.grid(row=1,column=3)
        ent_input_description = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)

        ent_input_description.insert(0.0,i[14])
        ent_input_description.grid(row=1,column=2,sticky=E)
        lbl_tak = CTkLabel(frame_moshkel,text=": نظر تکنسین",font=font)
        lbl_tak.grid(row=2,column=3)
        ent_tak = CTkTextbox(frame_moshkel,font=font_enry,corner_radius=10,width=400,height=100,border_width=3)
        ent_tak.insert(END,i[17])
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

        b = int(i[18])
        val = IntVar(value=b)
        chek_exit = CTkCheckBox(frame_moshkel,text="آماده تحویل",font=font,onvalue=1,variable=val,offvalue=0,)
        chek_exit.grid(row=2,column=0,sticky=E)
        
        abbbb = f'{i[15]}'
        str_ = StringVar(value=abbbb)
        chek = CTkCheckBox(frame_moshkel,30,text="بلی",font=font,onvalue="بلی",offvalue="خیر",variable=str_,command=modat)
        chek.grid(row=1,column=0,sticky=E)
        chek_2 = CTkCheckBox(frame_moshkel,30,text="خیر",font=font,onvalue="خیر",offvalue="بلی",variable=str_,command=modat)
        chek_2.grid(row=1,column=0,)



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
        conn = sqlite3.connect('database/pz.db')
        cursor = conn.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS ADMIN
                    (name_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    USER TEXT NOT NULL UNIQUE,
                    PASSWORD TEXT NOT NULL)''')
        cursor.execute("SELECT COUNT(*) FROM ADMIN")
        result = cursor.fetchone()
        if result[0] == 0:
            admin = [('admin', hash_password('7070816'))]
            cursor.executemany('INSERT INTO ADMIN(USER, PASSWORD) VALUES (?,?)', admin)
        conn.commit()
        conn.close()

    
    def login_admin():
        username = ent_user_login.get()
        password = ent_password_login.get()
        hashed_pass = hash_password(password)

        conn = sqlite3.connect('database/pz.db')
        cursor = conn.cursor()
        cursor.execute("SELECT PASSWORD FROM ADMIN WHERE USER=?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == hashed_pass:
            dashbord()
            messagebox.showinfo("ورود به سیستم", "با موفقیت وارد شدید.")
            global current_user
            current_user = username

        else:
            messagebox.showerror("مشکل", "نام کاربری یا رمز عبور نادرست است.")

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