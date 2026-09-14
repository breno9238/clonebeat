from pathlib import Path  # Importa a biblioteca para manipulação inteligente de caminhos de arquivos


# ==========================================
# GERENCIADOR DE NOTAS
# ==========================================
# Classe que lê, interpreta e converte o mapa de notas (geralmente gerado em arquivos .osu ou .ini) para o jogo de ritmo
class GerenciadorNotas:
    
    # Método construtor que recebe o arquivo contendo os tempos das notas e dispara a extração dos dados
    def __init__(self, arquivo_notas):
        
        self.arquivo_notas = Path(arquivo_notas)  # Converte o caminho recebido em um objeto Path do sistema
        self.data = self.carregar_notas_ini()  # Invoca a leitura do arquivo e armazena o resultado processado no atributo data
    
    # ==========================================
    # CARREGAR INI
    # ==========================================
    # Método responsável por ler as linhas do arquivo e decodificar o posicionamento temporal e espacial de cada nota
    def carregar_notas_ini(self):
        
        notas = []  # Inicializa uma lista vazia que irá colecionar as tuplas contendo tempo e coluna
        
        # Estrutura de contexto para abrir e garantir o fechamento seguro do arquivo com codificação universal utf-8
        with open(self.arquivo_notas, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()  # Lê todas as linhas do arquivo e as armazena sequencialmente em uma lista
        
        lendo_hitobjects = False  # Inicializa uma variável de controle (flag) para saber se está na seção certa de dados do arquivo
        
        # Laço de repetição que varre linha por linha do arquivo de notas extraído
        for linha in linhas:
            
            linha = linha.strip()  # Remove espaços em branco, quebras de linha (\n) ou tabulações inúteis do início e fim
            
            # Condicional que detecta o início da seção padrão que descreve os objetos de clique na tela
            if linha == '[HitObjects]':
                lendo_hitobjects = True  # Ativa a flag sinalizando que as próximas linhas válidas contêm dados das notas
                continue  # Avança imediatamente para o próximo ciclo do loop sem executar o código abaixo
            
            # Condicional que detecta se uma nova seção começou, indicando o fim da leitura dos objetos de clique
            if lendo_hitobjects and linha.startswith('['):
                break  # Interrompe completamente o laço de repetição for, encerrando o mapeamento
            
            # Condicional que assegura que a linha pertence à seção ativa, não está vazia e possui separação por vírgulas
            if lendo_hitobjects and linha and ',' in linha:
                
                partes   = linha.split(',')  # Divide a linha em vários pedaços usando a vírgula como caractere separador
                
                x_osu    = int(partes[0])  # Captura o primeiro valor da linha correspondente à coordenada horizontal nativa
                tempo_ms = int(partes[2])  # Captura o terceiro valor da linha correspondente ao instante de clique em milissegundos
                
                coluna   = min(max(int(x_osu / 128), 0), 3)  # Calcula matematicamente qual das 4 colunas (0 a 3) a nota pertence e limita o valor
                tempo    = tempo_ms / 1000  # Converte o tempo original de milissegundos para segundos reais com casas decimais
                
                notas.append((tempo, coluna))  # Adiciona uma tupla contendo o instante em segundos e o índice da coluna na lista coletora
        
        notas.sort(key=lambda n: n[0])  # Ordena toda a lista de notas com base no tempo de forma cronológica crescente
        return notas  # Retorna a lista final de notas perfeitamente estruturada e ordenada para a partida
