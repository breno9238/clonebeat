#__________________________________________________________________________________________________
# IMPORTAÇÃO DE DEPENDÊNCIAS
from pathlib import Path                    # Manipulação de arquivos e diretórios
from screens.gameplay import Gameplay      # Tela de jogabilidade do beatmap
from rules.beatmap_reader import Beatmap, ReadBeatmaps  # Leitura e representação de beatmaps
import customtkinter as ctk                # Interface gráfica moderna
import os                                   # Utilidades do sistema
import random                               # Funções aleatórias (não usado diretamente aqui)


#__________________________________________________________________________________________________
# TELA DO SELETOR DE BEATMAPS
class BeatmapsSelector(ctk.CTkFrame):
    """
    Frame principal que lista todos os beatmaps disponíveis.
    Permite expandir cada beatmap para ver suas dificuldades e iniciar o jogo.
    """
    
    #______________________________________________________________________________________________
    # CONSTRUTOR DO SELETOR
    def __init__(self, master):
        """
        Inicializa o frame do seletor e cria todos os cards de beatmaps.
        Parâmetros:
        master: widget pai (geralmente a janela principal)
        """
        # Inicializa o Frame principal do seletor
        super().__init__(
            master=master,
            corner_radius=0,
            fg_color='#1d1d1d',
            border_width=0
        )
        # Posiciona o frame para ocupar toda a área do pai
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        #__________________________________________________________________________________________
        # LISTA ROLÁVEL DE BEATMAPS
        # Contém os cards de beatmaps e permite rolagem vertical
        self.scroll_container = ctk.CTkScrollableFrame(
            master=self,                     # Pai: este frame do seletor
            corner_radius=10,                # Cantos arredondados
            fg_color='#2e2e2e',              # Cor de fundo do container
            scrollbar_fg_color='#555',       # Cor da barra de rolagem
            scrollbar_button_color="#575757" # Cor do botão da barra de rolagem
        )
        # Posiciona a lista rolável na parte direita da tela
        self.scroll_container.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        
        #__________________________________________________________________________________________
        # LEITOR DE BEATMAPS EXISTENTES
        # Lê os arquivos de beatmaps da pasta 'beatmaps'
        self.read = ReadBeatmaps('beatmaps')  
        
        # Lista que armazenará os cards principais de beatmaps
        self.cards = []  # Cada item será um BeatmapItem
        
        #__________________________________________________________________________________________
        # CRIAÇÃO DOS CARDS DE BEATMAP
        # Itera sobre todos os beatmaps lidos e cria visualmente os cards
        for beatmap in self.read.beatmaps.values():
            beatmap: Beatmap = beatmap # Converte para objeto Beatmap
            card = BeatmapItem(self.scroll_container, beatmap.difficults)  # Cria card principal
            self.cards.append(card)            # Adiciona à lista de cards
            
            # Cria subcards para cada dificuldade do beatmap
            for difficult in beatmap.difficults:
                data = beatmap.difficults[difficult]   # Dados da dificuldade
                
                # Cria item visual para a dificuldade
                secondary_card = DifficultItem(self.scroll_container, data)
                
                # Adiciona dificuldade ao card principal
                card.difficults.append(secondary_card)
                
                # Define atributos básicos do card principal
                card.audio_file = data['AudioFilename']
                card.title = data['Title']
                card.artist = data['Artist']
                card.creator = data['Creator']
                card.preview_time = data['PreviewTime']
                # Posiciona o card no topo da lista
                card.ui_show()
                card.pack(side='top', fill='x', padx=10, pady=10, expand=True)


#__________________________________________________________________________________________________
# ITEM DE BEATMAP PRINCIPAL (MAPA COMPLETO)
class BeatmapItem(ctk.CTkFrame):
    """
    Representa um card principal de beatmap.
    Pode ser expandido para mostrar suas dificuldades.
    """
    
    #______________________________________________________________________________________________
    # CONSTRUTOR DO ITEM PRINCIPAL
    def __init__(self, master, difficult):
        """
        Inicializa o card principal do beatmap.
        
        Parâmetros:
        master: widget pai (geralmente a lista rolável)
        """
        # Lista de dificuldades do beatmap (DifficultItem)
        self.difficults: list[DifficultItem] = []  # Inicialmente vazia
        
        # Atributos básicos do beatmap
        self.audio_file = None     # Arquivo de áudio principal
        self.title = None          # Título da música
        self.artist = None         # Artista
        self.creator = None        # Criador do beatmap
        self.preview_time = None   # Tempo de prévia da música
        self.is_open = False       # Indica se as dificuldades estão visíveis
        
        # Caixa principal do card (container visual)
        super().__init__(
            master=master,
            corner_radius=5,
            width=50,
            height=50,
            fg_color="#7d86bb",
            cursor='hand2'   # Cursor muda ao passar por cima
        )
        # Permite clicar no card para expandir ou recolher dificuldades
        self.bind('<Button-1>', self.select)
    
    def ui_show(self):
        #__________________________________________________________________________________________
        # WIDGETS DE INTERFACE (UI)
        
        # Decoração visual interna (label cinza)
        self.ui_background = ctk.CTkLabel(
            master=self,
            text='',
            corner_radius=10,
            fg_color='#808080'
        )
        self.ui_background.place(relx=0.5, rely=0.4, relwidth=0.25, relheight=0.1, anchor='center')
        self.ui_background.bind('<Button-1>', self.select)
        
        # Label do título
        self.ui_title = ctk.CTkLabel(
            master=self,
            text=self.title,
            font=('Roboto', 18, 'bold'),
            text_color='#FFFFFF'
        )
        self.ui_title.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.3, anchor='center')
        self.ui_title.bind('<Button-1>', self.select)
        
        # Label do artista
        self.ui_artist = ctk.CTkLabel(
            master=self,
            text=self.artist,
            font=('Roboto', 12, 'italic'),
            text_color='#CCCCCC',
            fg_color='black'
        )
        self.ui_artist.place(relx=0.6, rely=0.3, relwidth=0.9, relheight=0.3, anchor='center')
        self.ui_artist.bind('<Button-1>', self.select)
        
        # Label do criador
        self.ui_creator = ctk.CTkLabel(
            master=self,
            text=self.creator,
            font=('Roboto', 12, 'italic'),
            text_color='#CCCCCC',
            fg_color='black'
        )
        self.ui_creator.place(relx=0.6, rely=0.3, relwidth=0.9, relheight=0.3, anchor='center')
        self.ui_creator.bind('<Button-1>', self.select)
    
    #______________________________________________________________________________________________
    # FUNÇÃO PARA EXPANDIR/RECOLHER DIFICULDADES
    def select(self, event=None):
        """
        Mostra ou oculta os DifficultItems associados a este beatmap.
        """
        if not self.is_open:
            # Exibe todas as dificuldades
            for difficult in self.difficults:
                difficult.pack(side='top', fill='x', padx=50, pady=5, expand=True, after=self)
            self.is_open = True
        else:
            # Oculta todas as dificuldades
            for difficult in self.difficults:
                difficult.pack_forget()
            self.is_open = False


#__________________________________________________________________________________________________
# ITEM DE DIFICULDADE INDIVIDUAL (SUBCARD DO BEATMAP)
class DifficultItem(ctk.CTkFrame):
    """
    Representa uma dificuldade específica de um beatmap.
    Clicável para iniciar a jogabilidade.
    """
    
    #______________________________________________________________________________________________
    # CONSTRUTOR DO ITEM DE DIFICULDADE
    def __init__(self, master: ctk.CTk, difficult):
        
        self.difficult = difficult
        
        self.selected_diff = True
        
        # Caixa principal do item
        super().__init__(
            master=master,
            corner_radius=5,
            width=50,
            height=50,
            fg_color="#7d86bb",
            cursor='hand2'
        )
        self.bind('<Button-1>', self.select_diff)  # Inicia o jogo ao clicar
        
        # Decoração visual interna
        self.ui_background = ctk.CTkLabel(
            master=self,
            text='',
            corner_radius=10,
            fg_color='#808080'
        )
        self.ui_background.place(relx=0.5, rely=0.4, relwidth=0.25, relheight=0.1, anchor='center')
        self.ui_background.bind('<Button-1>', self.select_diff)
        
        # Label do título
        self.ui_title = ctk.CTkLabel(
            master=self,
            text=self.difficult['Version'],
            font=('Roboto', 18, 'bold'),
            text_color='#FFFFFF'
        )
        self.ui_title.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.3, anchor='center')
        self.ui_title.bind('<Button-1>', self.select_diff)
        
        # Label do artista
        self.ui_artist = ctk.CTkLabel(
            master=self,
            text=self.difficult['Artist'],
            font=('Roboto', 12, 'italic'),
            text_color='#CCCCCC',
            fg_color='black'
        )
        self.ui_artist.place(relx=0.6, rely=0.6, relwidth=0.9, relheight=0.3, anchor='center')
        self.ui_artist.bind('<Button-1>', self.select_diff)
        
        # Label do artista
        self.ui_creator = ctk.CTkLabel(
            master=self,
            text=self.difficult['Creator'],
            font=('Roboto', 12, 'italic'),
            text_color='#CCCCCC',
            fg_color='black'
        )
        self.ui_creator.place(relx=0.6, rely=0.9, relwidth=0.9, relheight=0.3, anchor='center')
        self.ui_creator.bind('<Button-1>', self.select_diff)
    
    #______________________________________________________________________________________________
    # FUNÇÃO PARA INICIAR JOGABILIDADE
    def select_diff(self, event=None):
        """
        Seleciona a difficuldade do beatmap e inicia a tela de Gameplay para este beatmap.
        """
        if not self.selected_diff:
            info = InfoBeatmapUI(
                self,                # Modo padrão
                self.audio_file,
                self.map_title,
                self.artist,
                self.creator,
                self.version,
                self.overall_difficulty,
                self.beatmap_id,
                self.circle_size,
                self.preview_time,
                self.hit_objects
                )
        
        if self.selected_diff:
            self.game = Gameplay(self.difficult)
            self.game.start()



class InfoBeatmapUI(ctk.CTkFrame):
    
    def __init__(
        self,
        master,                # Modo padrão
        audio_file,
        map_title,
        artist,
        creator,
        version,
        overall_difficulty,
        beatmap_id,
        circle_size,
        preview_time,
        hit_objects
        ):
        
        # Atributos principais do DifficultItem
        self.audio_file = audio_file
        self.map_title = map_title
        self.artist = artist
        self.creator = creator
        self.version = version
        self.overall_difficulty = overall_difficulty
        self.beatmap_id = beatmap_id
        self.circle_size = circle_size
        self.preview_time = preview_time
        self.hit_objects = hit_objects
        
        # Inicializa o Frame principal do seletor
        super().__init__(
            master=master,
            corner_radius=0,
            fg_color="#2e6a7c",     #1d1d1d
            border_width=0
        )
        # Posiciona o frame para ocupar toda a área do pai
        self.place(relx=0, rely=0, relwidth=0.4, relheight=1)