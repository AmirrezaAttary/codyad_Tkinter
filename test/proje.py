import tkinter as tk
import customtkinter
from customtkinter import *

class MyApp(CTk):
  def __init__(self):
    super().__init__()

    # Set Appearance and Theme
    self.DARK_MODE = "dark"
    customtkinter.set_appearance_mode(self.DARK_MODE)
    customtkinter.set_default_color_theme("dark-blue")

    # Font Settings
    self.font = CTkFont(family="Vazir", size=25, weight='bold')

    # Window Configuration
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure((0, 1, 2, 3), weight=0)
    self.grid_rowconfigure((4, 5, 6, 7), weight=1)
    self.overrideredirect(True)
    self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

    self.title("My Application") #Added for clarity
    self.dashbord() # Initialize with the dashboard

  def clear_frame(self):
    for widget in self.winfo_children():
      widget.destroy()

  def close_window(self):
    self.destroy()

  def dashbord(self):
    self.clear_frame()
    far = CTkFrame(self)
    far.grid(row=1, column=0, rowspan=7, sticky=NSEW)
    far.grid_columnconfigure(0, weight=1)
    far.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

    button_data = [
      ("پذیرش", self.paziresh_),
      ("گارانتی", self.garanti),
      ("ارسال پیامک", self.send_sms),
      ("تارخچه", self.tarikh_),
    ]
    for i, (text, command) in enumerate(button_data):
      button = customtkinter.CTkButton(far, text=text, font=self.font, command=command)
      button.grid(row=i + 1, column=0, padx=20, pady=20)

    btn_quit = customtkinter.CTkButton(far, text="خروج", fg_color='#EA0000', hover_color='#B20000', font=self.font, command=self.close_window)
    btn_quit.grid(row=len(button_data) + 1, column=0, padx=20, pady=0)

  def paziresh_(self):
    self.clear_frame()
    far_2 = CTkFrame(self)
    far_2.grid(row=1, column=0, rowspan=7, sticky=NSEW)
    far_2.grid_columnconfigure(0, weight=1)
    far_2.grid_rowconfigure((0, 1, 2, 3), weight=0)
    far_2.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame1 = customtkinter.CTkButton(far_2, text="dash", command=lambda: print("test dash"))
    bt_from_frame1.grid(row=0, column=0, padx=20, pady=(10, 0))
    bt_from_frame2 = customtkinter.CTkButton(far_2, text="dash 1", command=lambda: print("test dash 1"))
    bt_from_frame2.grid(row=1, column=0, padx=20, pady=(10, 0))
    bt_from_frame3 = customtkinter.CTkButton(far_2, text="بازگشت", font=self.font, command=self.dashbord)
    bt_from_frame3.grid(row=3, column=0, padx=20, pady=(10, 0))

  def create_return_button(self, return_command):
    self.clear_frame()
    far_4 = CTkFrame(self)
    far_4.grid(row=1, column=0, rowspan=7, sticky=NSEW)
    far_4.grid_columnconfigure(0, weight=1)
    far_4.grid_rowconfigure((0, 1, 2, 3), weight=0)
    far_4.grid_rowconfigure((4, 5, 6, 7), weight=1)
    bt_from_frame3 = customtkinter.CTkButton(far_4, text="بازگشت", font=self.font, command=return_command)
    bt_from_frame3.grid(row=7, column=0, padx=20, pady=(10, 0))

  def garanti(self):
    self.create_return_button(self.dashbord)

  def send_sms(self):
    self.create_return_button(self.dashbord)

  def tarikh_(self):
    self.create_return_button(self.dashbord)


if __name__ == "__main__":
  app = MyApp()
  app.mainloop()
