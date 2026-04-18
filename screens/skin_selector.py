from pathlib import Path
import customtkinter as ctk
from rules.skin_reader import SkinReader

class SkinSelector(ctk.CTkFrame):
    def __init__(self, master):
        
        
        
        super().__init__(
            master = master,
            corner_radius = 0,
            fg_color = "#1d1d1d",
            border_width = 0
        )
        
        self.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )
        
        self.read = SkinReader()

        self.scroll = ctk.CTkScrollableFrame(
            master=self,
            corner_radius=10,
            fg_color="#2e2e2e",
            scrollbar_fg_color="#555",
            scrollbar_button_color="#575757"
        )
        
        self.scroll.place(
            relx=0.6,
            rely=0,
            relwidth=0.4,
            relheight=1
        )
        
        for skins in self.read:
            frame = ctk.CTkFrame(
                master=self.scroll,
                
            )