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
            self.map_path = self.path
            self.save_data(self.path)
        
        elif self.path.suffix == '.osz':
            
            self.osz_file = self.path
            self.map_file = self.path.with_suffix('')
    
    def save_data(self, path):
        
        path_h = Path(path)
        
        if path_h.suffix == '.osz':
            
            try:
                # tenta criar a pasta do beatmap
                self.map_file.mkdir(parents=True, exist_ok=False)
                self.map_path = self.map_file 
                
                with zipfile.ZipFile(self.osz_file, 'r') as ziposz:
                    ziposz.extractall(self.map_file)
                    
                    # deleta o arquivo .osz após extrair
                    self.osz_file.unlink()
            
            except FileExistsError:
                # abre e extrai o conteúdo pra dentro da nova pasta e salva os dados uteis da extração
                with zipfile.ZipFile(self.osz_file, 'r') as ziposz:
                    ziposz.extractall(self.map_file)
        
        if path_h.is_dir():
            self.osu_files = list(self.path.glob('*.osu'))
            self.diff_names = list(i.name for i in self.osu_files)
            self.difficults = dict((i, None) for i in self.diff_names)
            self.music = next((self.path.glob('*.mp3')), None)
            self.background = next(self.path.glob('*.jpeg'), next(self.path.glob('*.png'), None))
            
            for arquive in self.osu_files: 
                
                osu_path = arquive
                self.difficults[arquive.name] = Difficult(osu_path, self.map_path)
    
    def is_diret(self):
            return self.path.is_dir()

class Difficult:
    
    def __init__(self, osu_path, osz_file):
        
        self.osu_path = Path(osu_path)
        self.notes = {}
        notes_section = False
        
        with open(self.osu_path, 'r', encoding='utf-8') as f:
                
                for line in f:
                    
                    if ':' in line:
                        
                        line = line.strip()
                        line_section = line.split(':', 1)
                        
                        match line_section[0]:
                            
                            case 'AudioFilename':
                                self.audio = line.removeprefix('AudioFilename: ')
                            
                            case 'Title':
                                self.title = line.removeprefix('Title: ')
                            
                            case 'Artist':
                                self.artist = line.removeprefix('Artist: ')
                            
                            case 'Creator':
                                self.mapper = line.removeprefix('Creator: ')
                            
                            case 'Version':
                                self.version = line.removeprefix('Version: ')
                            
                            case 'OverallDifficulty':
                                self.od = line.removeprefix('OverallDifficulty: ')
                            
                            case 'BeatmapID':
                                self.map_id = line.removeprefix('BeatmapID: ')
                            
                            case 'CircleSize':
                                self.key = line.removeprefix('CircleSize: ')
                            
                            case 'PreviewTime':
                                self.preview = line.removeprefix('PreviewTime: ')
                    
                    if not line:
                        continue
                    
                    if '[HitObjects]' in line:
                        
                        notes_section = True
                    
                    if notes_section:
                        
                        data = line.split(',')
                        
                        if len(data) >= 4 and ':' in line:
                            # x, y, tempo, tipo, hitSound, objetoParams
                            self.notes[data[2]] = data[0]