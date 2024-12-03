from customtkinter import *

root=CTk()

stik = NSEW

width = root.winfo_screenwidth() 
height = root.winfo_screenheight()

root.geometry(f'{width}x{height}+0+0')

root.grid_columnconfigure((0,1,2,3),weight=1)
#####################################################far0
far1=CTkFrame(
    root,
    fg_color='green',
)
far1.grid(
    column=0,
    row=0,
    columnspan=2,
    sticky=stik
)

far2=CTkFrame(
    root,
    fg_color='red',
)
far2.grid(
    column=2,
    row=0,
    sticky=stik
)

far3=CTkFrame(
    root,
    fg_color='aqua',
)
far3.grid(
    column=3,
    row=0,
    sticky=stik
)
#############################################far1
far4=CTkFrame(
    root,
    fg_color='#8B0000',
)
far4.grid(
    column=0,
    row=1,
    sticky=stik
)

far5=CTkFrame(
    root,
    fg_color='blue',
)
far5.grid(
    column=1,
    row=1,
    sticky=stik
)

far6=CTkFrame(
    root,
    fg_color='aqua',
)
far6.grid(
    column=2,
    row=1,
    sticky=stik
)

far7=CTkFrame(
    root,
    fg_color='red',
)
far7.grid(
    column=3,
    row=1,
    sticky=stik
)

########################################################################far2

far8=CTkFrame(
    root,
    fg_color='purple',
)
far8.grid(
    column=0,
    row=2,
    columnspan=2,
    rowspan=2,
    sticky=stik
)

far9=CTkFrame(
    root,
    fg_color='pink',
)
far9.grid(
    column=2,
    row=2,
    rowspan=2,
    sticky=stik
)

far10=CTkFrame(
    root,
    fg_color='magenta',
)
far10.grid(
    column=3,
    row=2,
    sticky=stik
)


####################################################far3

far11=CTkFrame(
    root,
    fg_color='yellow',
)
far11.grid(
    column=3,
    row=3,
    sticky=stik
)

root.mainloop()