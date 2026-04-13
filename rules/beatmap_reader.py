#-________IMPORTAÇÃO DE DEPENDÊNCIAS_____________________________________________________________
import zipfile                      # Biblioteca para descompactar arquivos .osz (formato zip)
from pathlib import Path            # Orientação a objetos para caminhos de arquivos e pastas



#-________LEITOR GERAL DE DIRETÓRIO (READBEATMAPS)__________________________________________________
class ReadBeatmaps:
    """
    Classe responsável por varrer a pasta de beatmaps,
    extrair arquivos .osz e criar instâncias de Beatmap.
    """
    
    def __init__(self, path: str):
        '''
        Inicializa a leitura de beatmaps.
        
        Argumentos:
            path (str): Caminho da pasta raiz contendo beatmaps.
        '''
        
        # Caminho da pasta "beatmaps"
        self.path: Path = Path(path)
        
        # Lista dos novos beatmaps adicionados que estõo compactados (.osz)
        self.new_maps: list[Path] = list(self.path.glob('*.osz'))
        
        # Lista vazia pra colocar os beatmaps extraidos depois
        self.beatmaps_list: list = []
        
        # Extrai cada arquivo .osz para uma pasta com mesmo nome sem sufixo
        for zip_file in self.new_maps:
            
            new_map: Path = zip_file.with_suffix('')      # Guarda o caminho do arquivo zip sem o sufixo ".osz"
            new_map.mkdir(parents=True, exist_ok=True)    # Cria nova pasta com o caminho novo guardado
            
            with zipfile.ZipFile(zip_file, 'r') as zip_r: # abre o arquivo .osz para leitura
                zip_r.extractall(new_map)                 # extrai os arquivos do .osz para a pasta nova
            zip_file.unlink()                             # Remove o arquivo .osz original
        
        # Cria dicionário de beatmaps já extraidos, incluindo os antigos e os novos
        # {Path(caminho): Beatmap(classe)}
        self.beatmaps: dict[Path, Beatmap] = {d: None for d in self.path.glob('*/')}
        
        # Percorre o dicionário de beatmaps pelas chaves
        for beatmap in self.beatmaps.keys():
            self.beatmaps[beatmap] = Beatmap(beatmap)               # Atribui a chave(ex: Rush E) a classe Beatmap
            self.beatmaps_list.append(self.beatmaps[beatmap])       # Guarda a classe criada para usar depois




#-________OBJETO DE DADOS DO BEATMAP (BEATMAP)______________________________________________________
class Beatmap:
    """
    Representa um beatmap completo, contendo metadados e dificuldades(.osu).
    """
    
    def __init__(self, beatmap: str | Path):
        """
        Inicializa o Beatmap.
        
        Argumentos:
            beatmap (str | Path): Caminho para a pasta do beatmap.
        """
        
        # Nome da pasta
        self.name: str = beatmap.stem    
        
        # Caminho da imagem do background
        self.background: Path | None = next(beatmap.glob('*.png'), next(beatmap.glob('*.jpeg'), next(beatmap.glob('*.jpg'), None)))
        
        # Cria dicionário de dificuldades {arquivo.osu: None inicialmente}
        self.difficults: dict[Path, dict] = {d: None for d in beatmap.glob('*.osu')}
         
        # Percorre cada dificuldade do mapa(.osu)
        for diff in self.difficults:
            
            # Variavel de controle para saber quando chegamos na seção de notas
            is_hit_objects_section: bool = False
            
            # Define cada dificuldade como um dicionário em difficults(dicionário)
            # self.difficults(dict) -> chave: Diff(ex: Hard), valor: dict(onde guarda informações)
            self.difficults[diff] = {}
            
            self.difficults[diff]['Background'] = self.background
            
            # Define que dentro de self.difficults(1° dict), na dificuldade atual(2° dict),
            # a chave 'HitObjects' tera como valor uma lista
            self.difficults[diff]['HitObjects'] = []
            
            # Abre o arquivo .osu em UTF-8(padrão) para leitura apenas
            with open(diff, 'r', encoding='utf-8') as text_file:
                
                # Percorre cada linha(line) do arquivo .osu(.txt disfarçado)
                for line in text_file:
                    
                    # Ignora linhas vazias
                    if not line:
                        continue  
                    
                    # Remove espaços em branco no começo e final das linhas
                    line = line.strip()
                    
                    # Leitura de metadados, procura por linhas com ":"(onde estão os dados
                    # em um formato parecido com dicionários) e garante que não está na sessão
                    # dos metadados das notas
                    if ':' in line and not is_hit_objects_section:
                        
                        # Separa cada linha em duas partes delimitadas pelo ":", ex:
                        # Title: Apollo -> strip(:) -> parts[0] = Title | parts[1] = Apollo
                        parts = line.split(':', 1)
                        
                        key_name = parts[0].strip()          # Guarda o nome da chave do metadado(ex: Title)
                        value_content = parts[1].strip()     # Guarda o valor do metadado (Ex: "Apollo")
                        
                        # Cria um atalho para acessar o dicionário vazio das informações de cada
                        # dificuldade (tipo o "tkinter as tk" )
                        diff_data = self.difficults[diff]     
                        
                        # Guarda o valor de cada campo/chave util em uma variavel
                        # Title: Apollo -> self.title = 'Apollo'
                        match key_name:
                            case 'AudioFilename':     diff_data['AudioFilename'] = Path(beatmap, value_content)
                            case 'Title':             diff_data['Title'] = value_content
                            case 'Artist':            diff_data['Artist'] = value_content
                            case 'Creator':           diff_data['Creator'] = value_content
                            case 'Version':           diff_data['Version'] = value_content
                            case 'OverallDifficulty': diff_data['OverallDifficulty'] = value_content
                            case 'BeatmapID':         diff_data['BeatmapID'] = value_content
                            case 'CircleSize':        diff_data['CircleSize'] = value_content
                            case 'PreviewTime':       diff_data['PreviewTime'] = value_content
                    
                    # Se encontrar [HitObjects] na linha, quer dizer que cada uma das proximas
                    # linhas representarão notas e irão guardar suas informações
                    if '[HitObjects]' in line:
                        is_hit_objects_section = True
                        continue
                    
                    # Se estiver na seção de HitObjects, extrai timestamp e posição X
                    if is_hit_objects_section:
                        
                        data_points = line.split(',')
                        
                        if len(data_points) >= 3:
                            
                            timestamp = int(data_points[2])      # Tempo da nota em ms(a partir do inicio da música)
                            pos_x = int(data_points[0])          # Posição X da nota(coluna)
                            
                            # guarda na lista 'HitObjects' uma tupla com o timestamp(tempo da
                            # música em que a nota aparece), e o pos_x(posição x em números
                            # que representa em qual das 4 colunas a nota está)
                            diff_notes: list = self.difficults[diff]['HitObjects']
                            diff_notes.append((timestamp, pos_x))



# Teste local pra listar todos os beatmaps atuais no terminal
if __name__ == '__main__':
    read_test = ReadBeatmaps('beatmaps')
    print('\nMAPAS:')
    for i in read_test.beatmaps:
        for a in read_test.beatmaps.values():
            print(f'''|  {i.name}\n| {a.difficults}''')
    print('')