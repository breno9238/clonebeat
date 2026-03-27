#-________IMPORTAÇÃO DE DEPENDÊNCIAS_____________________________________________________________
import zipfile                      # Biblioteca para descompactar arquivos .osz (formato zip)
from pathlib import Path            # Orientação a objetos para caminhos de arquivos e pastas



#-________LEITOR GERAL DE DIRETÓRIO (READBEATMAPS)__________________________________________________
class ReadBeatmaps:
    """
    Classe responsável por varrer o diretório raiz de beatmaps,
    extrair arquivos .osz e criar instâncias de Beatmap.
    """
    
    def __init__(self, path: str):
        """
        Inicializa a leitura de beatmaps.
        
        Args:
            path (str): Caminho da pasta raiz contendo beatmaps.
        """
        self.path: Path = Path(path)          # Caminho raiz
        self.beatmaps_list: list = []         # Lista de objetos Beatmap
        
        # Lista de novos pacotes compactados (.osz)
        self.new_maps: list[Path] = list(self.path.glob('*.osz'))
        
        # Extrai cada arquivo .osz para uma pasta com mesmo nome
        for zip_file in self.new_maps:
            new_map = zip_file.with_suffix('')         # Pasta de destino
            new_map.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(zip_file, 'r') as zip_r:
                zip_r.extractall(new_map)
            zip_file.unlink()                          # Remove o arquivo .osz original
        
        # Cria dicionário de beatmaps {pasta: Beatmap}
        self.beatmaps: dict[Path, Beatmap] = {d: None for d in self.path.glob('*/')}
        for bp in self.beatmaps:
            self.beatmaps[bp] = Beatmap(bp)           # Instância de Beatmap
            self.beatmaps_list.append(self.beatmaps[bp])


#-________OBJETO DE DADOS DO BEATMAP (BEATMAP)______________________________________________________
class Beatmap:
    """
    Representa um beatmap completo, contendo metadados e dificuldades (.osu).
    """
    
    def __init__(self, beatmap: str | Path):
        """
        Inicializa o Beatmap.
        
        Args:
            beatmap (str | Path): Caminho para a pasta do beatmap.
        """
        self.path: Path = Path(beatmap)                                  # Caminho do beatmap
        self.name: str = beatmap.name                                     # Nome da pasta
        self.background: Path | None = next(beatmap.glob('*.png'),       # Background opcional
                                           next(beatmap.glob('*.jpeg'), None))
        
        # Cria dicionário de dificuldades {arquivo.osu: None inicialmente}
        self.difficults: dict[Path, dict] = {d: None for d in beatmap.glob('*.osu')}
         
        # Percorre cada arquivo .osu e extrai metadados e notas
        for diff in self.difficults:
            
            # Flag de controle para saber quando chegamos na seção de notas
            is_hit_objects_section: bool = False
            
            # Inicializa dicionário de dados da dificuldade
            self.difficults[diff] = {}
            self.difficults[diff]['HitObjects'] = {}  # Dicionário {timestamp: pos_x}
            
            # Abre o arquivo .osu em UTF-8 para leitura linha a linha
            with open(diff, 'r', encoding='utf-8') as text_file:
                for line in text_file:
                    line = line.strip()  # Remove espaços em branco
                    
                    #---------------------------------------------------------------
                    # LEITURA DE METADADOS (KEY:VALUE)
                    if ':' in line and not is_hit_objects_section:
                        parts = line.split(':', 1)
                        key_name = parts[0].strip()          # Nome da chave
                        value_content = parts[1].strip()     # Valor
                        diff_data = self.difficults[diff]
                        
                        # Atribui os valores aos campos corretos usando match-case
                        match key_name:
                            case 'AudioFilename':     diff_data['AudioFilename'] = value_content
                            case 'Title':             diff_data['Title'] = value_content
                            case 'Artist':            diff_data['Artist'] = value_content
                            case 'Creator':           diff_data['Creator'] = value_content
                            case 'Version':           diff_data['Version'] = value_content
                            case 'OverallDifficulty': diff_data['OverallDifficulty'] = value_content
                            case 'BeatmapID':         diff_data['BeatmapID'] = value_content
                            case 'CircleSize':        diff_data['CircleSize'] = value_content
                            case 'PreviewTime':       diff_data['PreviewTime'] = value_content
                    
                    if not line:
                        continue  # Ignora linhas vazias
                    
                    #---------------------------------------------------------------
                    # LEITURA DE NOTAS (SEÇÃO [HitObjects])
                    if '[HitObjects]' in line:
                        is_hit_objects_section = True
                        continue
                    
                    # Se estiver na seção de HitObjects, extrai timestamp e posição X
                    if is_hit_objects_section:
                        data_points = line.split(',')
                        if len(data_points) >= 3:
                            timestamp = data_points[2]       # Tempo da nota em ms
                            pos_x = data_points[0]          # Posição X da nota
                            self.difficults[diff]['HitObjects'][timestamp] = pos_x


#___________________________________________________________________________________________________
# TESTE LOCAL
if __name__ == '__main__':
    read_test = ReadBeatmaps('beatmaps')
    lista = read_test.beatmaps.keys()
    for i in lista:
        print(f'''
            MAPAS:
            {i.name}
            ''')
        