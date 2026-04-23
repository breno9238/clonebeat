import customtkinter as ctk

class Menu(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title('Ritmo e Espada')
        self.geometry('800x520')
        
        self.play_button = ctk.CTkButton(
            master=self,
            text='JOGAR',
            
        )
        self.play_button.place(
            relx=0.5,
            rely=0.1,
            relwidth=0.25,
            relheight=0.1,
            anchor="center"
        )
        
        
        self.settings_button = ctk.CTkButton(
            master=self,
            text='CONFIGURAÇES'
        )
        
        self.settings_button.place(
            relx=0.5,
            rely=0.25,
            relwidth=0.25,
            relheight=0.1,
            anchor="center"
        )
        
        
        self.quit_button = ctk.CTkButton(
            master=self,
            text='QUIT'
        )
        self.quit_button.place(
            relx=0.5,
            rely=0.4,
            relwidth=0.25,
            relheight=0.1,
            anchor="center"
        )
        
        
        self.mainloop()