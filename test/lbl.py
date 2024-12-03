from customtkinter import *

window = CTk()


font = CTkFont(
    family='Vazir', # انتخاب فونت
    size=25, # سایزه فونت
    
)

lbl = CTkLabel( # ساختن لیبل
    window, # این که میخواهم در کدام صفحه وارد بشود
    # text='this is label', # متن داخل لیبل
    text='سلام به دوره خوش آمدید', # متن داخل لیبل به صورت فارسی
    width=60, # اندازه 
    height=40, # اندازه ارتفاع
    fg_color='red', # رنگ بک گراند متن
    text_color='black', # رنگ متن
    font=font, # دادن فونت به لیبل
)



lbl.pack()

window.geometry("500x400") # اندازه صفحه به صورت ماتریسی

window.mainloop()