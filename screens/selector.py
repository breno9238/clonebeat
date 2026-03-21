#________IMPORTAÇÃO DE DEPENDÊNCIAS___________________________
import customtkinter as ctk
from functools import partial
import pathlib
from pathlib import Path
import random
from PIL import Image
from screens.gameplay import Gameplay



#________FUNÇÃO DE GERAR COR ALEATÓRIA(HEX)___________________
def hexa_random():
    '''Gera um # e um numero aleatório entre 000000 e 16.777.215
    na formatação de hexadecimal(min = 000000 -> 0 max = 16.777.215 -> FFFFFF)'''
    
    return f'#{random.randint(0, 0xFFFFFF):06x}'



#________FRAME DO SELETOR DE BEATMAPS_________________________
class BeatmapsSelector(ctk.CTkFrame):
    
    #_____________________________________________________________
    #__CONSTRUTOR DO SELETOR____________________________
    def __init__(self, master):
        
        # frame do seletor
        super().__init__(
            master=master,             # Janela pai
            corner_radius=0,           # Cantos retos
            fg_color='#1d1d1d',    # Cor de fundo escura
            border_width=0,            # Sem borda
            border_color='gray'        # Cor da borda
            )
        # coloca o widget no lugar
        self.place(
            relx=0,                    # Encostado na esquerda
            rely=0,                    # Encostado no topo
            relwidth=1,                # Ocupa toda a largura (100%)
            relheight=1                # Ocupa toda a altura (100%)
        )
        
        
        
        #_____________________________________________________________
        #__LISTA ROLÁVEL DE BEATMAPS________________________
        self.beatmap_list = ctk.CTkScrollableFrame(     
            master=self,                            # Colocado dentro do seletor
            corner_radius=10,                       # Cantos arredondados
            fg_color='#2e2e2e',                 # Cinza grafite
            border_width=0,                         # Sem borda
            scrollbar_fg_color='#555',            # Cor da trilha da barra
            scrollbar_button_color="#575757"    # Cor do botão de rolagem
            )
        # coloca o widget no lugar
        self.beatmap_list.place(
            relx=0.6,                      # Inicia em 60% da largura
            rely=0,                        # Encostado no topo
            relwidth=0.4,                  # Ocupa os 40% restantes da tela
            relheight=1                    # Ocupa toda a altura
        )
        
        #_____________________________________________________________
        #__LEITOR DE BEATMAPS EXISTENTES________________________
        self.beatmaps_path = Path(__file__).parent.parent/'beatmaps'
        
        if self.beatmaps_path.exists():
            
            for beatmap in self.beatmaps_path.iterdir():
                
                color = hexa_random()
                
                if beatmap.is_dir():
                    
                    self.arquives = beatmap.glob('*')
                    map_file = next((a for a in self.arquives if a.suffix == '.osu'), None)
                    music_file = next((a for a in self.arquives if a.suffix == '.mp3'), None)
                    background_file = next((a for a in self.arquives if a.suffix == '.png' or a.suffix == 'png'), None)
                    
                    BeatmapItem(self.beatmap_list, color)



#________ITEM DO BEATMAP INDIVIDUAL NA LISTA__________________
class BeatmapItem(ctk.CTkFrame):
    
    #__CONSTRUTOR DO ITEM_______________________________
    def __init__(self, master):
        
        self.map_info = {
            'background': '',
            'title': 'Título Exemplo',
            'autor': 'Artista Exemplo',
            'beatmapper': 'Mapper Exemplo',
            'difficult': 'Hard',
            'difficulties': '',
            'song_preview': ''
        }
        
        
        
        #_____________________________________________________________
        #__CAIXA PRINCIPAL DO ITEM__________________________
        super().__init__(
            master=master,         # Janela pai (Lista rolável)
            corner_radius=5,           # Cantos pouco arredondados
            width=50,                  # Largura mínima
            height=50,                 # Altura fixa do card
            fg_color=hexa_random(),        # Cor aleatória do beatmap
            border_width=0,            # Sem borda
            cursor='hand2'             # Mouse vira mãozinha ao passar
        )
        # coloca o widget no lugar
        self.pack(
            side='top',                # Empilha de cima para baixo
            fill='x',                  # Estica na horizontal
            padx=10,                   # Afastamento das laterais
            pady=10,                   # Espaçamento entre itens
            expand=True                # Ajusta com o redimensionamento
        )
        self.bind('<Button-1>', self.play)
        
        
        
        #_____________________________________________________________
        #__FUNDO VISUAL DA CAIXA_____________________________
        self.background = ctk.CTkLabel(
            master=self,               # Colocado dentro do item
            text='',                   # Apenas fundo, sem texto
            corner_radius=10,          # Cantos arredondados
            fg_color=hexa_random()         # Segue a cor do card pai
        )
        # coloca o widget no lugar
        self.background.place(
            relx=0.5,                  # Centralizado horizontalmente (50%)
            rely=0.4,                  # Quase no meio da altura (40%)
            relwidth=0.25,             # Ocupa 1/4 da largura do card
            relheight=0.1,             # Ocupa 10% da altura do card
            anchor='center'            # Fixa o centro como referência
        )
        self.background.bind('<Button-1>', self.play)
        
        
        #_____________________________________________________________
        #__TÍTULO DA MÚSICA_________________________________
        self.title = ctk.CTkLabel(
            master=self,                    # Colocado dentro do card
            text=self.map_info['title'],    # Nome da música
            font=('Roboto', 18, 'bold'),    # Fonte moderna e em negrito
            text_color='#FFFFFF',           # Cor branca sólida
            corner_radius=0,                # Sem arredondamento
            width=200,                      # Largura definida
            height=30,                      # Altura definida
            justify='center'                # Centraliza o texto no label
        )
        # coloca o widget no lugar
        self.title.place(
            relx=0.5,                       # Centralizado horizontalmente (50%)
            rely=0.2,                       # Próximo ao topo (20%)
            relwidth=0.9,                   # Ocupa 90% da largura
            relheight=0.4,                  # Altura interna relativa
            anchor='center'                 # Fixa o centro como referência
        )
        self.title.bind('<Button-1>', self.play)
        
        
        
        #_____________________________________________________________
        #__AUTOR DA MÚSICA__________________________________
        self.autor = ctk.CTkLabel(
            master=self,                    # Colocado dentro do card
            text=self.map_info['autor'],    # Nome do artista
            font=('Roboto', 12, 'italic'),  # Fonte pequena e itálica
            text_color='#CCCCCC',           # Cinza claro para subtítulo
            corner_radius=5,                # Arredondamento do fundo
            fg_color='black'                # Fundo preto para destaque
        )
        # coloca o widget no lugar
        self.autor.place(
            relx=0.5,                       # Centralizado horizontalmente (50%)
            rely=0.5,                       # No meio da altura (50%)
            relwidth=0.3,                   # Largura interna relativa
            relheight=0.15,                 # Altura interna relativa
            anchor='center'                 # Fixa o centro como referência
        )
        self.autor.bind('<Button-1>', self.play)
        
        
        
        #_____________________________________________________________
        #__BEATMAPPER DO MAPA_______________________________
        self.beatmapper = ctk.CTkLabel(
            master=self,                                   # Colocado dentro do card
            text=f"Mapper: {self.map_info['beatmapper']}", # Texto formatado
            font=('Roboto', 10),                           # Fonte discreta
            text_color='#AAAAAA',                      # Cor cinza suave
            fg_color='transparent'                          # Sem fundo colorido
        )
        # coloca o widget no lugar
        self.beatmapper.place(
            relx=0.5,                            # Centralizado horizontalmente (50%)
            rely=0.75,                           # Parte inferior (75%)
            relwidth=0.8,                        # Largura interna relativa
            relheight=0.1,                       # Altura interna relativa
            anchor='center'                      # Fixa o centro como referência
        )
        self.beatmapper.bind('<Button-1>', self.play)
    
    def play(self, event=None):
        self.game = Gameplay('padrão', [])