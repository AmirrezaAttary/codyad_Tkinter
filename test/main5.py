import tkinter
import tkinter.messagebox
import customtkinter
from PIL import Image
import os

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class Page(customtkinter.CTkFrame):
    def __init__(self):
        customtkinter.CTkFrame.__init__()
    def show(self):
        self.lift()
            
class Page1(Page):
    def __init__(self):
        Page.__init__()

class HomePage(customtkinter.CTkFrame):
   def __init__(self):
        super().__init__()
        
        self.title("IMS")
        self.geometry(f"{1300}x{800}")
        
        self.rowconfigure((0), weight=1)
        self.columnconfigure((0), weight=1)
        self.rowconfigure((1, 2), weight=1)     
        self.columnconfigure((1,2), weight=1)   
        self.rowconfigure((3), weight=1)
        
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.logoImage = customtkinter.CTkImage(Image.open(os.path.join(image_path, "os.jpg")), size=(150, 66))        
        
        self.titleLogo = customtkinter.CTkLabel(master=self, text="", image=self.logoImage)
        self.titleLogo.grid(row=0, column=1, padx=0, pady=0)
        
        self.categoriesButton = customtkinter.CTkButton(master=self, border_width=2, text_color=("gray10", "#DCE4EE"),font=("",33), width=150, height=50, text="Categories", command=Page1.show())
        self.categoriesButton.grid(row=2, column=0, padx=(50, 50), pady=(0, 40), sticky="nsew", columnspan=3)
        



if __name__ == "__main__":
    app = HomePage()
    app.mainloop()