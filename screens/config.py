#________IMPORTAÇÃO DE DEPENDÊNCIAS___________________________
import customtkinter as ctk



#________TELA DE CONFIGURAÇÕES DO JOGO________________________
class Config(ctk.CTkFrame):
    
    #_____________________________________________________________
    #__CONSTRUTOR E CONFIGURAÇÃO DO FRAME_______________
    def __init__(self, par_master):
        
        super().__init__(
            master=par_master,             # Janela pai
            width=200,                     # Largura inicial
            height=200,                    # Altura inicial
            corner_radius=10,              # Arredondamento dos cantos
            fg_color='#1d1d1d',            # Cor de fundo escura
            border_width=0,                # Sem borda
            border_color='gray'            # Cor da borda
            )
    
    
    
    #_____________________________________________________________
    #__RENDERIZAÇÃO DA TELA NA JANELA___________________
    def render(self):
        
        # coloca o widget no lugar
        self.place(
            relx=0,                        # Encostado na esquerda
            rely=0,                        # Encostado no topo
            relwidth=1,                    # Ocupa toda a largura (100%)
            relheight=1                    # Ocupa toda a altura (100%)
        )
