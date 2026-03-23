#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import customtkinter as ctk                  # Interface Gráfica
import os                                    # Sistema de Arquivos
import random                                # Gerador de Aleatórios
from pathlib import Path                     # Caminhos de Diretório
from screens.gameplay import Gameplay           
from rules.beatmap_reader import Beatmap, Difficult  



#________FUNÇÃO DE GERAR COR ALEATÓRIA (HEX)________________________________________________________
def hexa_random() -> str:
    '''Gera uma cor em formato hexadecimal para a interface.'''
    return f'#{random.randint(0, 0xFFFFFF):06x}'



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
        self.directory_beatmaps = Path(__file__).parent.parent / 'beatmaps'
        
        if self.directory_beatmaps.exists():
            
            # folder_path: Deixa claro que é o caminho da pasta sendo iterada
            for folder_path in self.directory_beatmaps.iterdir():
                
                # map_data: Representa o objeto lógico do mapa carregado
                map_data = Beatmap(folder_path)
                
                if map_data.is_diret():
                    
                    # diff_file: Nome do arquivo de dificuldade (string)
                    for diff_file in map_data.difficults:
                        
                        caminho_completo = os.path.join(folder_path, diff_file)
                        
                        # diff_obj: Representa o objeto da dificuldade específica
                        diff_obj = Difficult(caminho_completo, folder_path)
                    
                    #_______________________________________________________________________________
                    # CRIAÇÃO DO COMPONENTE VISUAL
                    # map_card: Nome padrão para itens de interface em lista
                    self.map_card = BeatmapItem(
                        master=self.scroll_container,
                        map_ref=map_data,
                        audio_path=diff_obj.audio_fn,
                        title_text=diff_obj.song_title,
                        artist_text=diff_obj.song_artist,
                        mapper_name=diff_obj.mapper_name,
                        version_name=diff_obj.diff_version,
                        od_value=diff_obj.od_value,
                        key_count=diff_obj.key_count,
                        map_id=diff_obj.map_uid,
                        cover_path=diff_obj.preview_ms,
                        )



#________ITEM DO BEATMAP INDIVIDUAL NA LISTA________________________________________________________
class BeatmapItem(ctk.CTkFrame):
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DO ITEM (BEATMAP)____________________________________________________________________
    def __init__(
        self, 
        master: ctk.CTkScrollableFrame, 
        map_ref: Beatmap, 
        audio_path: str, 
        title_text: str, 
        artist_text: str, 
        mapper_name: str, 
        version_name: str, 
        od_value: float, 
        key_count: int, 
        map_id: int, 
        cover_path: str
    ):
        
        # ATRIBUTOS LÓGICOS (DADOS)
        self.map_ref: Beatmap = map_ref
        self.audio_file: str = audio_path
        self.title_str: str = title_text
        self.artist_str: str = artist_text
        self.mapper_str: str = mapper_name
        self.version_str: str = version_name
        self.od: float = od_value
        self.keys: int = key_count
        self.uid: int = map_id
        self.cover_file: str = cover_path
        
        
        #___________________________________________________________________________________________
        #__CAIXA PRINCIPAL DO ITEM (CONTAINER)______________________________________________________
        super().__init__(
            master=master,
            corner_radius=5,
            width=50,
            height=50,
            fg_color=hexa_random(),
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
            fg_color=hexa_random()
        )
        self.ui_background_decor.place(relx=0.5, rely=0.4, relwidth=0.25, relheight=0.1, anchor='center')
        self.ui_background_decor.bind('<Button-1>', self.play)
        
        
        # ui_title_label: Rótulo de texto do título
        self.ui_title_label = ctk.CTkLabel(
            master=self,
            text=self.title_str,
            font=('Roboto', 18, 'bold'),
            text_color='#FFFFFF'
        )
        self.ui_title_label.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.3, anchor='center')
        self.ui_title_label.bind('<Button-1>', self.play)
        
        
        # ui_artist_label: Rótulo de texto do artista
        self.ui_artist_label = ctk.CTkLabel(
            master=self,
            text=self.artist_str,
            font=('Roboto', 12, 'italic'),
            text_color='#CCCCCC',
            fg_color='black'
        )
    
    def play(self):
        self.game = Gameplay()