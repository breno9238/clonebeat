#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import customtkinter as ctk                  # Interface Gráfica
import os                                    # Sistema de Arquivos
import random                                # Gerador de Aleatórios
from pathlib import Path                     # Caminhos de Diretório
from screens.gameplay import Gameplay          
from rules.beatmap_reader import Beatmap, ReadBeatmaps 



#________FRAME DO SELETOR DE BEATMAPS_______________________________________________________________
class BeatmapsSelector(ctk.CTkFrame):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DO SELETOR________________________________________________________________________
    def __init__(self, master):
        
        # Inicialização do Frame Principal
        super().__init__(
            master=master,
            corner_radius=0,
            fg_color='#1d1d1d',
            border_width=0
            )
        
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        
        #___________________________________________________________________________________________
        #__LISTA ROLÁVEL DE BEATMAPS________________________________________________________________
        # scroll_container: Nome que indica que o widget guarda outros itens com rolagem
        self.scroll_container = ctk.CTkScrollableFrame(     
            master=self,
            corner_radius=10,
            fg_color='#2e2e2e',
            scrollbar_fg_color='#555',
            scrollbar_button_color="#575757"
            )
        
        self.scroll_container.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        
        
        #___________________________________________________________________________________________
        #__LEITOR DE BEATMAPS EXISTENTES____________________________________________________________
        self.read = ReadBeatmaps('beatmaps')
        
        self.cards = []
        
        #_______________________________________________________________________________
        # CRIAÇÃO DO COMPONENTE VISUAL
        # map_card: Nome padrão para itens de interface em lista
        for map_obj in self.read.beatmaps.values():
            mapp: Beatmap = map_obj
            for bpd in mapp.difficults:
                
                diff_data = mapp.difficults[bpd]
                
                card = BeatmapItem(
                    master=self.scroll_container,
                    audio_file_name=diff_data['AudioFilename'],
                    map_title=diff_data['Title'],
                    artist=diff_data['Artist'],
                    creator=diff_data['Creator'],
                    version=diff_data['Version'],
                    overall_difficulty=diff_data['OverallDifficulty'],
                    beatmap_id=diff_data['BeatmapID'],
                    circle_size=diff_data['CircleSize'],
                    preview_time=diff_data['PreviewTime'],
                    hit_objects=diff_data['HitObjects']
                    )
                self.cards.append(card)



#________ITEM DO BEATMAP INDIVIDUAL NA LISTA________________________________________________________
class BeatmapItem(ctk.CTkFrame):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DO ITEM (BEATMAP)____________________________________________________________________
    def __init__(
        self,
        master: ctk.CTk,
        audio_file_name: str,
        map_title: str,
        artist: str,
        creator: str,
        version: str,
        overall_difficulty: str,
        beatmap_id: str,
        circle_size: str,
        preview_time: str,
        hit_objects: dict[int, int]
        
    ):
        
        self.audio_file_name = audio_file_name
        self.map_title = map_title
        self.artist = artist
        self.creator = creator
        self.version = version
        self.overall_difficulty = overall_difficulty
        self.beatmap_id = beatmap_id
        self.circle_size = circle_size
        self.preview_time = preview_time
        self.hit_objects = hit_objects
        
        #___________________________________________________________________________________________
        #__CAIXA PRINCIPAL DO ITEM (CONTAINER)______________________________________________________
        super().__init__(
            master=master,
            corner_radius=5,
            width=50,
            height=50,
            fg_color="#bb7d7d",
            cursor='hand2'
        )
        
        self.pack(side='top', fill='x', padx=10, pady=10, expand=True)
        self.bind('<Button-1>', self.play)
        
        
        #___________________________________________________________________________________________
        #__WIDGETS DE INTERFACE (UI)________________________________________________________________
        
        # ui_background_decor: Decoração visual interna
        self.ui_background_decor = ctk.CTkLabel(
            master=self,
            text='', 
            corner_radius=10,
            fg_color='#808080'
        )
        self.ui_background_decor.place(relx=0.5, rely=0.4, relwidth=0.25, relheight=0.1, anchor='center')
        self.ui_background_decor.bind('<Button-1>', self.play)
        
        
        # ui_title_label: Rótulo de texto do título
        self.ui_title_label = ctk.CTkLabel(
            master=self,
            text=map_title,
            font=('Roboto', 18, 'bold'),
            text_color='#FFFFFF'
        )
        self.ui_title_label.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.3, anchor='center')
        self.ui_title_label.bind('<Button-1>', self.play)
        
        
        # ui_artist_label: Rótulo de texto do artista
        self.ui_artist_label = ctk.CTkLabel(
            master=self,
            text=artist,
            font=('Roboto', 12, 'italic'),
            text_color='#CCCCCC',
            fg_color='black'
        )
        self.ui_artist_label.place(relx=0.6, rely=0.3, relwidth=0.9, relheight=0.3, anchor='center')
        self.ui_artist_label.bind('<Button-1>', self.play)
    
    def play(self, event=None):
        self.game = Gameplay(
            'padrão',
            audio_file_name=self.audio_file_name,
            map_title=self.map_title, 
            artist=self.artist,
            creator=self.creator, 
            version=self.version,
            overall_difficulty=self.overall_difficulty,
            beatmap_id=self.beatmap_id,
            circle_size=self.circle_size,
            preview_time=self.preview_time,
            hit_objects=self.hit_objects
        )