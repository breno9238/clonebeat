#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
from screens.selector_beatmap import BeatmapsSelector   # Tela de seleção de músicas
from screens.config import Config               # Tela de configurações do sistema
import tkinter as tk                            # Biblioteca base do Tk
import customtkinter as ctk                     # Framework de UI moderna



#________CLASSE PRINCIPAL DA APLICAÇÃO______________________________________________________________
class App(ctk.CTk):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR E CONFIGURAÇÃO DA UI______________________________________________________________
    def __init__(self):
        '''Inicializa a janela principal e as configurações básicas do CloneBeat.'''
        
        super().__init__()
        
        # Parâmetros Físicos da Janela
        self.title('CloneBeat')                 # Título da barra superior
        self.geometry('900x600')                # Resolução inicial
        self.config(bg="#1d1d1d")               # Cor de fundo base
        
        # Carregamento de Atributos Visuais
        # self.icone: Armazena o objeto PhotoImage para o ícone da barra de tarefas
        self.icone: tk.PhotoImage = tk.PhotoImage(file='images/clonebeat_icon.png')
        self.iconphoto(True, self.icone)
        
        
        
        #___________________________________________________________________________________________
        #__FRAME DO MENU INICIAL____________________________________________________________________
        # menu_ui: Container principal que abriga os botões do lobby
        self.menu_ui: ctk.CTkFrame = ctk.CTkFrame(  
            master=self,                        # Raiz da aplicação
            width=200,                          # Largura base
            height=200,                         # Altura base
            corner_radius=10,                   # Arredondamento suave
            fg_color="#1d1d1d",                 # Mantém o cinza escuro
            border_width=0,                     # Sem contorno visível
            border_color="gray"                 # Cor de borda reserva
        )
        
        # Posicionamento Relativo (Ocupa a tela toda)
        self.menu_ui.place(
            relx=0,                             # Início na esquerda
            rely=0,                             # Início no topo
            relwidth=1,                         # 100% da largura
            relheight=1                         # 100% da altura
        )
        
        
        
        #___________________________________________________________________________________________
        #__BOTÃO JOGAR______________________________________________________________________________
        self.jogar_button: ctk.CTkButton = ctk.CTkButton(
            master=self.menu_ui,                # Localizado dentro do menu
            text='JOGAR',                       # Label central
            width=200,                          # Largura fixa do botão
            height=40,                          # Altura fixa do botão
            command=self.show_selector,         # Callback para troca de tela
            fg_color="#5F9EA0",                 # Azul Petróleo
            hover_color="#4F8485",              # Destaque ao passar o mouse
            text_color="white"                  # Fonte branca para leitura
        )
        
        self.jogar_button.place(
            relx=0.5,                           # Centro horizontal
            rely=0.1,                           # 10% de distância do topo
            relwidth=0.25,                      # 1/4 da tela de largura
            relheight=0.1,                      # 10% da tela de altura
            anchor='center'                     # Ponto de ancoragem no centro
        )
        
        
        
        #___________________________________________________________________________________________
        #__BOTÃO CONFIGURAÇÕES______________________________________________________________________
        self.configurações_button: ctk.CTkButton = ctk.CTkButton(
            master=self.menu_ui,                
            text='CONFIGURAÇÕES',               
            width=200,                          
            height=40,                          
            command=self.show_config,           
            fg_color="#5F9EA0",        
            hover_color="#4F8485",     
            text_color="white"             
        )
        
        self.configurações_button.place(
            relx=0.5,                      
            rely=0.25,                          # Abaixo do botão Jogar
            relwidth=0.25,                 
            relheight=0.1,                 
            anchor='center'                
        )
        
        
        
        #___________________________________________________________________________________________
        #__BOTÃO SAIR_______________________________________________________________________________
        self.sair_button: ctk.CTkButton = ctk.CTkButton(
            master=self.menu_ui,              
            text='SAIR',                   
            width=200,                     
            height=40,                     
            command=self.destroy,               # Encerra o processo da aplicação
            fg_color="#5F9EA0",        
            hover_color="#4F8485",     
            text_color="white"             
        )
        
        self.sair_button.place(
            relx=0.5,                      
            rely=0.4,                           # Abaixo das configurações
            relwidth=0.25,                 
            relheight=0.1,                 
            anchor='center'                
        )
    
    
    #_______________________________________________________________________________________________
    #__EXIBE A TELA DE SELEÇÃO DE MAPAS_____________________________________________________________
    def show_selector(self):
        '''Instancia o Seletor de Beatmaps sobrepondo o menu principal.'''
        self.selector: BeatmapsSelector = BeatmapsSelector(self)
    
    
    #_______________________________________________________________________________________________
    #__EXIBE A TELA DE CONFIGURAÇÕES________________________________________________________________
    def show_config(self):
        '''Instancia o Frame de Configurações sobrepondo o menu principal.'''
        self.config: Config = Config(self)
