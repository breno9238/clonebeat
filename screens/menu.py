import customtkinter as ctk
from .beatmap_selector import PhaseSelector
from .settings_selector import SettingsSelector

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
            command=self.show_phase_selector
            
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
            text='CONFIGURAÇES',
            command=self.show_settings_selector
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
            text='QUIT',
            command=self.destroy
        )
        self.quit_button.place(
            relx=0.5,
            rely=0.4,
            relwidth=0.25,
            relheight=0.1,
            anchor="center"
        )
    
    def show_phase_selector(self):
        self.phase_selector = PhaseSelector(self)
    
    def show_settings_selector(self):
        self.settings_selector = SettingsSelector(self)