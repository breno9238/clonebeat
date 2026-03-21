#________IMPORTAÇÃO DE DEPENDÊNCIAS___________________________
import zipfile
from pathlib import Path



#________LEITOR E CRIADOR DE BEATMAP___________________________
class Beatmap:
    
    #_____________________________________________________________
    #__CONSTRUTOR DO LEITOR_____________________________
    def __init__(self, beatmap):
        
        self.beatmap = beatmap                                 # Nome do beatmap passado como argumento
        self.path = Path(f'beatmaps/{beatmap}')                 # Define o caminho do diretório do mapa
        
        #_____________________________________________________________
        #__VARREDURA DE ARQUIVOS____________________________
        
        for file in self.path.iterdir():                       # Percorre os arquivos na pasta do mapa
            
            # se for uma pasta já extraida
            if file.is_dir(): 
                self.save_data()
            
            # se for um novo mapa pra extrair
            elif self.path.suffix == '.osz':
                
                osz_file = self.path                   # Referência ao arquivo compactado .osz
                map_file = osz_file.with_suffix('')    # Caminho da pasta que será criada
                
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
                    # deleta o arquivo se a pasta já existe
                    osz_file.unlink()
    
    def save_data(self):
        
        self.arquives = self.path.glob('*')            # Captura todos os arquivos presentes
        # captura os arquivos úteis
        
        chart_file = next((a for a in self.arquives if a.suffix == '.osu'), None)
        self.content = chart_file.read_text(encoding='utf-8')
        
        with open(''):
        
        
        self.music = next((a for a in self.arquives if a.suffix == '.mp3'), None)
        
        # guarda arquivo d
        self.background = next((a for a in self.arquives if a.suffix in ['.png', '.jpg']), None)