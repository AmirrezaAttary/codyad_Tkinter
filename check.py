from customtkinter import *
from tkinter.messagebox import showinfo

window = CTk()

window.geometry('500x500') # اندازه صفحه به صورت ماتریسی

# def check_amir():
#     test = check.get()
#     showinfo(test,test)

def check_box_():
    if check.get() == 'ok':
        text_var.set(value='im ok in this time')
    else:
        text_var.set(value='im not ok in this time')
    
state_var=StringVar(value='ok')
text_var=StringVar(value='im ok')

check = CTkCheckBox(
    window,
    text='are you ok',
    onvalue='ok',
    offvalue='not ok',
    # command=check_amir,
    variable=state_var,
    command=check_box_,
    textvariable=text_var,
    checkbox_height=50,
    checkbox_width=50
)
check.pack()

def del_():
    check.deselect()

btn_del = CTkButton(
    window,
    text="delete",
    command=del_
)
btn_del.pack(pady=20)

def sel_():
    check.deselect()
    text_var.set(value='im not ok in this time')

btn_sel = CTkButton(
    window,
    text='select',
    command=sel_
)
btn_sel.pack(pady=15)


window.mainloop()