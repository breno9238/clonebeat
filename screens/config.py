#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import customtkinter as ctk        # Framework de interface moderna (UI)



#________TELA DE CONFIGURAÇÕES DO JOGO______________________________________________________________
class Config(ctk.CTkFrame):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR E CONFIGURAÇÃO DO FRAME___________________________________________________________
    def __init__(self, par_master: any):
        '''
        Inicializa o container principal da tela de configurações.
        par_master: A janela ou frame principal (App) que conterá esta tela.
        '''
        
        # Inicialização do Widget CTkFrame
        super().__init__(
            master=par_master,             # Define o elemento pai
            width=200,                     # Largura base (ajustada no render)
            height=200,                    # Altura base (ajustada no render)
            corner_radius=10,              # Cantos arredondados suavizados
            fg_color='#1d1d1d',            # Cor de fundo (Cinza Chumbo)
            border_width=0,                # Sem contorno de borda
            border_color='gray'            # Cor da borda (inativa se width=0)
            )
    
    
    
    #_______________________________________________________________________________________________
    #__RENDERIZAÇÃO DA TELA NA JANELA_______________________________________________________________
    def render(self):
        '''
        Gerencia o posicionamento e a visibilidade da tela no layout.
        Utiliza coordenadas relativas para manter a responsividade.
        '''
        
        # Posicionamento Dinâmico (Layout Total)
        self.place(
            relx=0,                        # Alinhado ao canto esquerdo (0%)
            rely=0,                        # Alinhado ao topo (0%)
            relwidth=1,                    # Estica para ocupar 100% da largura
            relheight=1                    # Estica para ocupar 100% da altura
        )
