#________IMPORTAÇÃO DE DEPENDÊNCIAS___________________________
import zipfile
from pathlib import Path



#________LEITOR E CRIADOR DE BEATMAP___________________________
class Beatmap:
    
    #_____________________________________________________________
    #__CONSTRUTOR DO LEITOR_____________________________
    def __init__(self, beatmap):
        
        self.path = Path(beatmap)                 # Define o caminho da pasta do mapa
        
        #_____________________________________________________________
        #__VARREDURA DE ARQUIVOS____________________________
        
        if self.path.is_dir():                                  # Percorre os arquivos na pasta do mapa
            self.save_data()
        
        elif self.path.suffix == '.osz':
            
            osz_file = self.path
            map_file = self.path.with_suffix('')
            
            try:
                # tenta criar a pasta do beatmap
                map_file.mkdir(parents=True, exist_ok=False)
                
                # abre e extrai o conteúdo pra dentro da nova pasta e salva os dados uteis da extração
                with zipfile.ZipFile(osz_file, 'r') as ziposz:
                    ziposz.extractall(map_file)
                self.save_data()
                
                # deleta o arquivo .osz após extrair
                osz_file.unlink()
            
            except FileExistsError:
                    # abre e extrai o conteúdo pra dentro da nova pasta e salva os dados uteis da extração
                    with zipfile.ZipFile(osz_file, 'r') as ziposz:
                        ziposz.extractall(map_file)
                    self.save_data()
    
    def save_data(self):
        
        self.osu_files = list(self.path.glob('*.osu'))
        self.diff_names = list(i.name for i in self.osu_files)
        self.difficults = dict((i, None) for i in self.diff_names)
        self.music = next((self.path.glob('*.mp3')), None)
        self.background = next(self.path.glob('*.jpeg'), next(self.path.glob('*.png'), None))
        
        for arquive in self.osu_files: 
            
            self.difficults[arquive.name] = Difficult(arquive)
    
    def is_diret(self):
            return self.path.is_dir()

class Difficult:
    
    def __init__(self, osu_path):
        
        osu_path
        
        with open(osu_path, 'r', encoding='utf-8') as f:
                
                for line in f:
                    
                    if ':' in line:
                        
                        line = line.strip()
                        line_section = line.split(':', 1)
                        
                        match line_section[0]:
                            
                            case 'AudioFilename':
                                self.audio_name = line.removeprefix('AudioFilename: ')
                            
                            case 'Title':
                                self.title = line.removeprefix('Title: ')
                            
                            case 'Creator':
                                self.mapper = line.removeprefix('Creator: ')
                            
                            case 'Artist':
                                self.artist = line.removeprefix('Artist: ')
                            
                            case 'Version':
                                self.difficulties = line.removeprefix('Version: ')
                            
                            case 'OverallDifficulty':
                                self.overalldiff = line.removeprefix('OverallDifficulty: ')
                            
                            case 'BeatmapID':
                                self.id = line.removeprefix('BeatmapID: ')