from customtkinter import *

window = CTk()

width = window.winfo_screenwidth()
height = window.winfo_screenheight()

btn = CTkButton(window,text='click me')
btn.pack()

window.geometry(f'{width}x{height}+0+0')
# window.geometry(f'{width}x{height}')


# window.after(0,lambda :window.state('zoomed'))

# window.wm_attributes('-fullscreen', True)

# window.state('zoomed')

window._set_appearance_mode("system")

window.mainloop()