#________IMPORTAÇÃO DE DEPENDÊNCIAS_________________________________________________________________
import zipfile                      # Biblioteca para descompactar arquivos .osz (formato zip)
from pathlib import Path            # Orientação a objetos para caminhos de arquivos e pastas



#___________________________________________________________________________________________________
#________FLUXOGRAMA LÓGICO DE PROCESSAMENTO_________________________________________________________
#  
#     [ENTRADA: Caminho do Beatmap]
#      .
#      ├──> [class ReadBeatmaps] ....................... Varredura de arquivos no diretório root
#      │    • .../beatmaps/ -> list(glob('*.osz')) ..... Coleta pacotes compactados
#      .
#      └──> [class Beatmap] ........................... Gerenciamento de integridade e extração
#           • entry_path: str|Path .................... Recebe endereço
#           .
#           ├──> [process_folder_data] ................ Fluxo de descompactação
#           │    • if .osz: ........................... Extrai conteúdo via ZipFile
#           │    • if .is_dir: ........................ Mapeia mídias (.mp3, .png, .jpeg)
#           │    • if .osu: ........................... Dispara instâncias de [Difficult]
#           │    • .................................... Retorno: dict(Dificuldades)
#           .
#           └──> [class Difficult] .................... Dificuldades = arquivos .osu(txt)
#                • open(file, 'utf-8') ................ Leitura de texto
#                .
#                ├──> .osu(txt) -> [Metadados] ........ Identifica chaves (Key:Value)
#                │    • Case Match .................... Atribui: (audio, título, od, keys)
#                .
#                └──> .osu(txt) -> [HitObjects] ....... Mapeia as notas do jogo
#                     • split(',') .................... Extrai x(coluna), y(onde nasce), time(ms)
#                     • ............................... Retorno: notes_data{timestamp: pos_x}
#  
#___________________________________________________________________________________________________



#-________LEITOR GERAL DE DIRETÓRIO__________________________________________________________________
class ReadBeatmaps():
    
    def __init__(self, path: str):
        
        # Define a pasta raiz onde os mapas do jogo ficam armazenados
        self.path: Path = Path(path)
        self.beatmaps_list = []
        
        # Faz uma busca (glob) por todos os arquivos com extensão .osz na pasta raiz
        self.new_maps: list[Path] = list(self.path.glob('*.osz'))
        for zip in self.new_maps:
            new_map = zip.with_suffix('')
            new_map.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip, 'r') as zip_r:
                zip_r.extractall(new_map)
            zip.unlink()
        
        self.beatmaps: dict[Path, None] = {d: None for d in self.path.glob('*/')}
        for bp in self.beatmaps:
            self.beatmaps[bp] = Beatmap(bp)
            self.beatmaps_list.append(self.beatmaps[bp])



#________OBJETO DE DADOS DO BEATMAP_________________________________________________________________
class Beatmap:
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DO MAPA___________________________________________________________________________
    def __init__(self, beatmap: str | Path):
        
        self.path: Path = Path(beatmap)
        self.name: str = beatmap.name
        self.background: Path | None = next(beatmap.glob('*.png'), next(beatmap.glob('*.jpeg'), None))
        
        self.difficults: dict = {d: None for d in beatmap.glob('*.osu')}
        
        # Percorre a lista de arquivos .osu e cria uma instância da classe Difficult para cada um
        for diff in self.difficults: 
            
            # Flag de controle para saber quando chegamos na seção de notas do arquivo
            is_hit_objects_section: bool = False
            
            self.difficults[diff] = {}
            
            self.difficults[diff]['HitObjects'] = {}
            
            # Abre o arquivo para leitura linha por linha (UTF-8 evita erros com caracteres especiais)
            with open(diff, 'r', encoding='utf-8') as text_file:
                
                for line in text_file:
                    line = line.strip() 
                    
                    #_______________________________________________________________________________
                    #__LEITURA DE METADADOS (ESTRUTURA CHAVE: VALOR)________________________________
                    if ':' in line and not is_hit_objects_section:
                        
                        parts = line.split(':', 1) 
                        key_name = parts[0].strip()
                        value_content = parts[1].strip()
                        
                        match key_name:
                            case 'AudioFilename':     self.difficults[diff]['AudioFilename'] = value_content
                            case 'Title':             self.difficults[diff]['Title'] = value_content
                            case 'Artist':            self.difficults[diff]['Artist'] = value_content
                            case 'Creator':           self.difficults[diff]['Creator'] = value_content
                            case 'Version':           self.difficults[diff]['Version'] = value_content
                            case 'OverallDifficulty': self.difficults[diff]['OverallDifficulty'] = value_content
                            case 'BeatmapID':         self.difficults[diff]['BeatmapID'] = value_content
                            case 'CircleSize':        self.difficults[diff]['CircleSize'] = value_content
                            case 'PreviewTime':       self.difficults[diff]['PreviewTime'] = value_content
                    
                    if not line:
                        continue
                    
                    #_______________________________________________________________________________
                    #__LEITURA DE NOTAS (SEÇÃO [HitObjects])________________________________________
                    if '[HitObjects]' in line:
                        is_hit_objects_section = True 
                        continue
                    
                    if is_hit_objects_section:
                        data_points = line.split(',')
                        if len(data_points) >= 3:
                            timestamp = data_points[2]
                            pos_x = data_points[0]
                            self.difficults[diff]['HitObjects'][timestamp] = pos_x

if __name__ == '__main__':
    
    read_test = ReadBeatmaps('beatmaps')
    print(read_test.beatmaps)