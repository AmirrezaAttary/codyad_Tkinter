from customtkinter import *

window = CTk()

window.geometry('500x500')


color_list = ['red','blue','green']
combo = CTkComboBox(
    window,
    values=color_list,
    corner_radius=50,
    # font=CTkFont(size=25),
    dropdown_fg_color='red',
    dropdown_text_color='blue',
)
combo.pack(pady=15)

entry = CTkEntry(
    window,
    placeholder_text='Enter color'
)
entry.pack(pady=15)

def set_():
    color= entry.get()
    color_list.append(color)
    combo.configure(values=color_list)

btn_set_color = CTkButton(
    window,
    text='set_color',
    command=set_
)
btn_set_color.pack(pady=15)
window.mainloop()