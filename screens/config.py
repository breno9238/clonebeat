#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import customtkinter as ctk        # Framework de interface moderna (UI)
from screens.skin_selector import SkinSelector


#________TELA DE CONFIGURAÇÕES DO JOGO______________________________________________________________
class Config(ctk.CTkFrame):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR E CONFIGURAÇÃO DO FRAME___________________________________________________________
    def __init__(self, master):
        '''
        Inicializa o container principal da tela de configurações.
        par_master: A janela ou frame principal (App) que conterá esta tela.
        '''
        
        # Inicialização do Widget CTkFrame
        super().__init__(
            master=master,             # Define o elemento pai
            width=200,                     # Largura base (ajustada no render)
            height=200,                    # Altura base (ajustada no render)
            corner_radius=10,              # Cantos arredondados suavizados
            fg_color='#1d1d1d',            # Cor de fundo (Cinza Chumbo)
            border_width=0,                # Sem contorno de borda
            border_color='gray'            # Cor da borda (inativa se width=0)
            )
        
        # Posicionamento Dinâmico (Layout Total)
        self.place(
            relx=0,                        # Alinhado ao canto esquerdo (0%)
            rely=0,                        # Alinhado ao topo (0%)
            relwidth=1,                    # Estica para ocupar 100% da largura
            relheight=1                    # Estica para ocupar 100% da altura
        )
        
        self.skins_buttom = ctk.CTkButton(
            master=self,
            text="SKINS",
            width=200,
            height=40,
            corner_radius=7,
            command=self.show_skin_selector,
            bg_color="#1d1d1d",
            fg_color="#5F9EA0",
            hover_color="#4F8485",
            text_color="white"
        )
        
        self.skins_buttom.place(
            relx=0.5,
            rely=0.1,
            relwidth=0.25,
            relheight=0.1,
            anchor="center"
        )
        
        self.voltar_buttom = ctk.CTkButton(
            master=self,
            text="VOLTAR",
            width=200,
            height=40,
            corner_radius=7,
            command=self.voltar_menu,
            bg_color="#1d1d1d",
            fg_color="#5F9EA0",
            hover_color="#4F8485"
        )
        
        self.voltar_buttom.place(
            relx=0.5,
            rely=0.25,
            relwidth=0.25,
            relheight=0.1,
            anchor="center"
        )
        
        
        
    
    
    
    def show_skin_selector(self):
        
        self.skin_selector : SkinSelector = SkinSelector(self)
        self.skin_selector.lift()
    
    def voltar_menu(self):
        self.skins_buttom.destroy()
        self.voltar_buttom.destroy()
        self.destroy()

    