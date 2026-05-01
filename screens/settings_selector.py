import customtkinter as ctk

class SettingsSelector(ctk.CTkFrame):
    
    def __init__(self, root: ctk.CTk):
        
        super().__init__(master=root)
        
        self.place(relx=0, rely=0, relwidth=1, relheight=1)