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
class ReadBeatmaps:
    
    def __init__(self):
        # Define a pasta raiz onde os mapas do jogo ficam armazenados
        self.main_path_dir: Path = Path('beatmaps')
        
        # Faz uma busca (glob) por todos os arquivos com extensão .osz na pasta raiz
        self.osz_files_list: list[Path] = list(self.main_path_dir.glob('*.osz'))
        self.extracted_files_list: list[Path] = list(self.main_path_dir.glob(' */'))
        
        if self.osz_files_list:
            for osz_file in self.osz_files_list:
                self.new_extracted_file: Path = osz_file.replace('.osz', '')
                try:
                    self.new_extracted_file.mkdir(parents=False, exist_ok=False)
                
                except FileExistsError:
                    pass
                
                finally:
                    with zipfile.ZipFile(osz_file, 'r') as zip_ref:
                        zip_ref.extractall(self.new_extracted_file)
                    osz_file.unlink()
                    self.process_folder_data(self.new_extracted_file)
        
        if self.extracted_files_list:
            for extracted_file in self.extracted_files_list:
                self.process_folder_data(extracted_file)
    
    #_______________________________________________________________________________________________
    #__GERENCIAMENTO DE ARQUIVOS____________________________________________________________________
    def process_folder_data(self, current_path: Path):
        
        # Localiza todos os arquivos de configuração de dificuldade do mapa
        self.osu_files_list: list[Path] = list(current_path.glob('*.osu'))
        
        # Prepara o dicionário que guardará os objetos de cada dificuldade
        self.diff_dict: dict[str, any] = {file.name: None for file in self.osu_files_list}
        
        # Tenta localizar o primeiro arquivo de áudio disponível (.mp3)
        self.audio_file: Path | None = next(current_path.glob('*.mp3'), None)
        
        # Busca imagens de fundo (tenta .jpeg, se não achar tenta .png)
        self.bg_image: Path | None = next(
            current_path.glob('*.jpeg'), 
            next(current_path.glob('*.png'), None))
        
        # Percorre a lista de arquivos .osu e cria uma instância da classe Difficult para cada um
        for osu_file in self.osu_files_list: 
            # Associa o nome do arquivo ao objeto de dados processado
            self.diff_dict[osu_file.name] = Difficult(osu_file, current_path)
    
    def is_diret(self) -> bool:
        return self.entry_path.is_dir()



#________OBJETO DE DADOS DO BEATMAP_________________________________________________________________
class Beatmap:
    
    #_______________________________________________________________________________________________
    #__CONSTRUTOR DO MAPA___________________________________________________________________________
    def __init__(self, beatmap_path: str | Path):
        
        # Converte a entrada em um objeto Path para facilitar manipulações futuras
        self.entry_path: Path = Path(beatmap_path)
        
        #___________________________________________________________________________________________
        #__VARREDURA E PROCESSAMENTO________________________________________________________________
        
        # Caso a entrada já seja uma pasta extraída
        if self.entry_path.is_dir():
            self.map_folder_path: Path = self.entry_path     # Define como a pasta oficial do mapa
            self.process_folder_data(self.entry_path)        # Inicia leitura dos arquivos internos
        
        
        # Caso a entrada seja um arquivo compactado .osz
        elif self.entry_path.suffix == '.osz':
            self.compressed_file: Path = self.entry_path     # Guarda referência do arquivo zip
            self.target_folder: Path = self.entry_path.with_suffix('') # Define nome da nova pasta
            self.process_folder_data(self.entry_path)        # Inicia extração e leitura


#________OBJETO DE DADOS DA DIFICULDADE_____________________________________________________________
class Difficult:
    
    def __init__(self, osu_file_path: Path, parent_folder: Path):
        
        # Caminho do arquivo de texto (.osu) que contém as notas e metadados
        self.osu_path: Path = Path(osu_file_path)
        
        # Dicionário para armazenar as notas: {tempo_em_ms: posicao_x}
        self.notes_data: dict[str, str] = {} 
        
        # Flag de controle para saber quando chegamos na seção de notas do arquivo
        is_hit_objects_section: bool = False
        
        # Abre o arquivo para leitura linha por linha (UTF-8 evita erros com caracteres especiais)
        with open(self.osu_path, 'r', encoding='utf-8') as file_content:
                
                for line in file_content:
                    line = line.strip() 
                    
                    #_______________________________________________________________________________
                    #__LEITURA DE METADADOS (ESTRUTURA CHAVE: VALOR)________________________________
                    if ':' in line and not is_hit_objects_section:
                        
                        parts = line.split(':', 1) 
                        key_name = parts[0].strip()
                        value_content = parts[1].strip()
                        
                        match key_name:
                            case 'AudioFilename':     self.audio_fn: str = value_content
                            case 'Title':             self.song_title: str = value_content
                            case 'Artist':            self.song_artist: str = value_content
                            case 'Creator':           self.mapper_name: str = value_content
                            case 'Version':           self.diff_version: str = value_content
                            case 'OverallDifficulty': self.od_value: str = value_content
                            case 'BeatmapID':         self.map_uid: str = value_content
                            case 'CircleSize':        self.key_count: str = value_content
                            case 'PreviewTime':       self.preview_ms: str = value_content
                    
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
                            self.notes_data[timestamp] = pos_x
