from customtkinter import *

window = CTk()

window.geometry('500x500')


controller_var = IntVar(value=0)
gender_male = CTkRadioButton(
    window,
    text='male',
    value=1,
    variable=controller_var,
)
gender_male.pack(side='right')

gender_female = CTkRadioButton(
    window,
    text='female',
    value=2,
    variable=controller_var,
)
gender_female.pack(side='right')

window.mainloop()