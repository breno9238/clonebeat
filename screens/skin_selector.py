import customtkinter as ctk
from pathlib import Path
from rules.skin_reader import SkinReader

class SkinSelector(ctk.CTkFrame):
    def __init__(self, master):
        
        self.master = master
        self.skin_itens = []
        
        super().__init__(
            master = master,
            corner_radius = 10,
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
        
        self.voltar_buttom = ctk.CTkButton(
            master=self,
            text="VOLTAR",
            width=200,
            height=40,
            corner_radius=7,
            command=self.voltar_config,
            bg_color="#1d1d1d",
            fg_color="#5F9EA0",
            hover_color="#4F8485"
        )
        
        self.voltar_buttom.place(
            relx=0.2,
            rely=0.1,
            relwidth=0.25,
            relheight=0.1,
            anchor="center"
        )
        
        
        
        
        
        for skin in self.read.skins_list:
            item = SkinItem(self.scroll, skin)
            self.skin_itens.append(item)
    
    def voltar_config(self):
        self.master.focus()
        self.destroy()
        


class SkinItem(ctk.CTkFrame):
    def __init__(self, master, skin):
        
        self.skin = skin
        
        super().__init__(
            master=master,
                height=100
        )
        
        self.pack(
                side='top',
                fill='x',
                padx=10,
                pady=10,
                expand=True
            )
        
        
        self.skin_title = ctk.CTkLabel(
            master=self,
            text=self.skin.name  #mudar depois para uma variavel do nome da skin
        )
        
        self.skin_title.place(
            relx=0.5,
            rely=0.1,
            relwidth=0.4,
            relheight=0.1,
            anchor="center"
        )
        
        
        
        









class SkinInfo:  # esta classe serve para mostrar as imagems das keys logo abaixo de cada skin quando clicado
    def __init__(self):
        pass