import customtkinter as ctk

class SettingsSelector(ctk.CTkFrame):
    
    def __init__(self, root: ctk.CTk):
        
        super().__init__(master=root)
        
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        self.buttom = ctk.CTkButton(
            master=self,
            text="VOLTAR",
            command=self.back_menu,
            corner_radius=10,
            
            
        )
        
        self.buttom.place(
            rely=0.1,
            relx=0.1,
            relwidth=0.2,
            relheight=0.1
        )
    
    def back_menu(self):
        self.destroy()