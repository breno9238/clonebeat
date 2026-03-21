#________IMPORTAÇÃO DE DEPENDÊNCIAS___________________________
from screens.selector import BeatmapsSelector
from screens.config import Config
import tkinter as tk
import customtkinter as ctk



#________CLASSE PRINCIPAL DA APLICAÇÃO________________________
class App(ctk.CTk):
    
    #__CONSTRUTOR E CONFIGURAÇÃO DA UI__________________
    def __init__(self):
        
        super().__init__()
        
        # Configuração da janela
        self.title('CloneBeat')
        self.geometry('900x600')
        self.config(bg="#1d1d1d")
        
        # Carregamento do ícone
        self.icone = tk.PhotoImage(file='images/clonebeat_icon.png')
        self.iconphoto(True, self.icone)
        
        
        
        #_____________________________________________________________
        #__FRAME DO MENU INICIAL____________________________
        self.menu = ctk.CTkFrame(  
            master=self,                   # Janela pai
            width=200,                     # Largura inicial
            height=200,                    # Altura inicial
            corner_radius=10,              # Arredondamento dos cantos
            fg_color="#1d1d1d",        # Cor de fundo escura
            border_width=0,                # Grossura da borda
            border_color="gray"            # Cor da borda
        )
        # coloca o widget no lugar
        self.menu.place(
            relx=0,                        # Encostado na esquerda
            rely=0,                        # Encostado no topo
            relwidth=1,                    # Ocupa toda a largura (100%)
            relheight=1                    # Altura relativa (100% da janela)
        )
        
        
        
        #_____________________________________________________________
        #__BOTÃO JOGAR______________________________________
        self.jogar_button = ctk.CTkButton(
            master=self.menu,              # Frame pai
            text='JOGAR',                  # Texto do botão
            width=200,                     # Largura fixa
            height=40,                     # Altura fixa
            command=self.show_selector,    # Abre o seletor de mapas
            fg_color="#5F9EA0",        # Cor do botão (Azul petróleo)
            hover_color="#4F8485",     # Cor ao passar o mouse
            text_color="white"             # Cor da fonte
        )
        # coloca o widget no lugar
        self.jogar_button.place(
            relx=0.5,                      # Centralizado horizontalmente (50%)
            rely=0.1,                      # Próximo ao topo (10%)
            relwidth=0.25,                 # Ocupa 1/4 da largura do pai
            relheight=0.1,                 # Ocupa 10% da altura do pai
            anchor='center'                # Fixa o centro como referência
        )
        
        
        
        #_____________________________________________________________
        #__BOTÃO CONFIGURAÇÕES______________________________
        self.configurações_button = ctk.CTkButton(
            master=self.menu,              # Frame pai
            text='CONFIGURAÇÕES',          # Texto do botão
            width=200,                     # Largura fixa
            height=40,                     # Altura fixa
            command=self.show_config,      # Abre as configurações
            fg_color="#5F9EA0",        # Cor do botão (Azul petróleo)
            hover_color="#4F8485",     # Cor ao passar o mouse
            text_color="white"             # Cor da fonte
        )
        # coloca o widget no lugar
        self.configurações_button.place(
            relx=0.5,                      # Centralizado horizontalmente (50%)
            rely=0.25,                     # Abaixo do botão Jogar (25%)
            relwidth=0.25,                 # Ocupa 1/4 da largura do pai
            relheight=0.1,                 # Ocupa 10% da altura do pai
            anchor='center'                # Fixa o centro como referência
        )
        
        
        
        #_____________________________________________________________
        #__BOTÃO SAIR_______________________________________
        self.sair_button = ctk.CTkButton(
            master=self.menu,              # Frame pai
            text='SAIR',                   # Texto do botão
            width=200,                     # Largura fixa
            height=40,                     # Altura fixa
            command=self.destroy,          # Fecha o programa
            fg_color="#5F9EA0",        # Cor do botão (Azul petróleo)
            hover_color="#4F8485",     # Cor ao passar o mouse
            text_color="white"             # Cor da fonte
        )
        # coloca o widget no lugar
        self.sair_button.place(
            relx=0.5,                      # Centralizado horizontalmente (50%)
            rely=0.4,                      # Abaixo das configurações (40%)
            relwidth=0.25,                 # Ocupa 1/4 da largura do pai
            relheight=0.1,                 # Ocupa 10% da altura do pai
            anchor='center'                # Fixa o centro como referência
        )
    
    
    #__EXIBE A TELA DE SELEÇÃO DE MAPAS_________________
    def show_selector(self):
        self.selector = BeatmapsSelector(self)
    
    
    #__EXIBE A TELA DE CONFIGURAÇÕES____________________
    def show_config(self):
        self.config = Config(self)
