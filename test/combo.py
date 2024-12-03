from customtkinter import *
import customtkinter

window = CTk()
window.geometry('500x500')


state_var=StringVar(value='system')
mod_list = ['dark', 'light', 'system']

# def get_():
#     x = combo.get()
#     print(x)
    

def choise_(choice):
    # print(choice)
    customtkinter.set_appearance_mode(choice)

combo = CTkComboBox(
    window,
    values=mod_list,
    variable=state_var,
    command=choise_
)
combo.pack(pady=20)

# btn = CTkButton(
#     window,
#     text="submit",
#     command=get_
# )
# btn.pack(pady=20)

window.mainloop()