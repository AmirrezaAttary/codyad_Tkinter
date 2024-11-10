from customtkinter import *

window = CTk()

width = window.winfo_screenwidth() # گرفتن ساز مانیتور
height = window.winfo_screenheight() # گرفتن ساز مانیتور

btn = CTkButton(window,text='click me',command=window.destroy)
btn.pack()

window.geometry(f'{width}x{height}+0+0') # فول اسکرن کردن با این ها صورت میگیرد
# window.geometry(f'{width}x{height}') # فول اسکرن کردن با این ها صورت میگیرد


# window.after(0,lambda :window.state('zoomed')) # فول اسکرن کردن با این ها صورت میگیرد

# window.wm_attributes('-fullscreen', True)

# window.state('zoomed') # فول اسکرن کردن با این ها صورت میگیرد

window._set_appearance_mode("system")

window.mainloop()