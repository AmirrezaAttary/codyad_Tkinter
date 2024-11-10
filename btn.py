from customtkinter import *



window = CTk()

window.title('amir')

window.geometry('500x400')

def click():
    print('گی')

btn = CTkButton( # ساختن دکمه
    window, # این که میخواهم در کدام صفحه وارد بشود
    #width=45, # اندازه 
    #height=10, # اندازه ارتفاع
    text='Click me', # تکست داخل دکمه
    corner_radius=50, # گرد کردن حاشیه های هر چیزی
    border_width=3, # اندازه بردر دور هر چیزی
    border_color='black', # رنگ بردر دور
    #border_spacing=6, # فاصله داخلی بردر
    fg_color='red', # رنگ هم با اسم هم با کد کالر
    hover_color='pink', # رنگ هاور
    text_color= 'black', # رنگ تکست
    #image= '', # آوردن عکس در هرجا
    #state='disable', # از کار انداختن 
    #hover=False, # استفاده از هاور آره یا نه
    command=click, # دادن دستور
    
)

btn.pack()

window.mainloop()