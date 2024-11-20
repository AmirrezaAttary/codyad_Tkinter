import tkinter
import customtkinter
from customtkinter import *

DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("dark-blue")

##########################################################################################
root = CTk()
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure((0, 1, 2, 3), weight=0)
root.grid_rowconfigure((4, 5, 6, 7), weight=1)
root.overrideredirect(True)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

font = CTkFont(family="Vazir",size=25,weight='bold')
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
    far.grid_rowconfigure(( 0, 1, 2, 3, 4,5, 6, 7), weight=1)
    bt_dashboard = customtkinter.CTkButton(far, text="پذیرش",font=font, command=paziresh_)
    bt_dashboard.grid(row=1 ,column=0, padx=20, pady=20)

    bt_sms = customtkinter.CTkButton(far, text="گارانتی",font=font, command=garanti)
    bt_sms.grid(row=2 ,column=0, padx=20, pady=20)

    bt_sms = customtkinter.CTkButton(far, text="ارسال پیامک",font=font, command=send_sms)
    bt_sms.grid(row=3 ,column=0, padx=20, pady=20)

    bt_tarikh = customtkinter.CTkButton(far, text="تارخچه",font=font, command=tarikh_)
    bt_tarikh.grid(row=4 ,column=0, padx=20, pady=20)

    btn_quit = customtkinter.CTkButton(far, text="خروج", fg_color= '#EA0000', hover_color = '#B20000',font=font, command= close_window)
    btn_quit.grid(row=5, column=0, padx=20, pady=0)



def paziresh_():
    clear_frame()
    far_2 = CTkFrame(root)
    far_2.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_2.grid_columnconfigure(0, weight=1)
    far_2.grid_rowconfigure((0, 1, 2, 3), weight=0)
    far_2.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_2, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=3, column=0, padx=20, pady=(10, 0))
    
    
def garanti():
    far_4 = CTkFrame(root)
    far_4.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_4.grid_columnconfigure(0, weight=1)
    far_4.grid_rowconfigure((0, 1, 2, 3), weight=0)
    far_4.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_4, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=7, column=0, padx=20, pady=(10, 0))
    

def send_sms():
    far_3 = CTkFrame(root)
    far_3.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_3.grid_columnconfigure(0, weight=1)
    far_3.grid_rowconfigure((0, 1, 2, 3), weight=0)
    far_3.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_3, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=7, column=0, padx=20, pady=(10, 0))
    

def tarikh_():
    far_4 = CTkFrame(root)
    far_4.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
    far_4.grid_columnconfigure(0, weight=1)
    far_4.grid_rowconfigure((0, 1, 2, 3), weight=0)
    far_4.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_4, text="بازگشت",font=font, command=dashbord)
    bt_from_frame3.grid(row=7, column=0, padx=20, pady=(10, 0))

###########################################################################################
far = CTkFrame(root)
far.grid(row=1, column=0,rowspan=7, sticky=NSEW)    
far.grid_columnconfigure(0, weight=1)
# far.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
far.grid_rowconfigure(( 0, 1, 2, 3, 4, 5, 6, 7), weight=1)

bt_dashboard = customtkinter.CTkButton(far, text="پذیرش",font=font, command=paziresh_)
bt_dashboard.grid(row=1 ,column=0, padx=20, pady=20)

bt_sms = customtkinter.CTkButton(far, text="گارانتی",font=font, command=garanti)
bt_sms.grid(row=2 ,column=0, padx=20, pady=20)

bt_sms = customtkinter.CTkButton(far, text="ارسال پیامک",font=font, command=send_sms)
bt_sms.grid(row=3 ,column=0, padx=20, pady=20)

bt_tarikh = customtkinter.CTkButton(far, text="تارخچه",font=font, command=tarikh_)
bt_tarikh.grid(row=4 ,column=0, padx=20, pady=20)

btn_quit = customtkinter.CTkButton(far, text="خروج", fg_color= '#EA0000', hover_color = '#B20000',font=font, command= close_window)
btn_quit.grid(row=5, column=0, padx=20, pady=0)


root.mainloop()