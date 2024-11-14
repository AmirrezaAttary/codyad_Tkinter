from customtkinter import *

window = CTk()

window.geometry("500x500")

def male_female():
    if gender_male.get()=='male':
        gender_female.deselect()
    elif gender_male.get()=='female':
        gender_male.deselect()

gender_male=CTkCheckBox(
    window,
    text='male',
    onvalue='male',
    offvalue='off',
    command=male_female
)
gender_male.pack(side='right')

gender_female=CTkCheckBox(
    window,
    text='female',
    onvalue='female',
    offvalue='off',
    command=male_female
)
gender_female.pack(side='right')


window.mainloop()