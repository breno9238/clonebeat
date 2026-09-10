import configparser  # Importa o leitor de arquivos de configuração no formato .ini

from pathlib import Path  # Importa a biblioteca para manipulação inteligente de caminhos de arquivos

import arcade  # Importa a biblioteca gráfica Arcade para o jogo de ritmo


# ==========================================
# GERENCIADOR DE SKINS
# ==========================================
# Classe responsável por ler o arquivo de configuração da skin e carregar todas as texturas das notas e botões
class GerenciadorSkin:
    
    # Método construtor que inicializa o gerenciador definindo os atributos e chamando os carregadores
    def __init__(self, pasta_skin):
        
        self.pasta_skin = Path(pasta_skin)  # Converte o caminho recebido em um objeto Path do sistema
        
        self.texturas_receptor = []  # Inicializa a lista que guardará as texturas dos botões receptores neutros
        self.texturas_receptor_clicado = []  # Inicializa a lista para as texturas dos botões em estado pressionado
        self.texturas_notas    = []  # Inicializa a lista que guardará as imagens das notas em movimento
        self.nome              = None  # Inicializa a variável que armazenará o nome estético da skin
        self.largura_nota = None  # Inicializa a propriedade que define a largura padrão das notas de ritmo
        self.altura_nota = None  # Inicializa a propriedade que define a altura padrão das notas de ritmo
        
        self.largura_receptor = None  # Inicializa a dimensão horizontal própria dos botões de acerto
        self.altura_receptor = None  # Inicializa a dimensão vertical própria dos botões de acerto
        
        self.carregar_skin_ini()  # Invoca o método interno que lê os parâmetros do arquivo skin.ini
        self.carregar_texturas()  # Invoca o método interno que carrega e redimensiona as imagens PNG
    
    # ==========================================
    # RETORNA ARQUIVO
    # ==========================================
    # Método auxiliar que constrói o caminho absoluto para um arquivo específico dentro da pasta da skin
    def obter_arquivo(self, nome_arquivo):
        
        arquivo_skin = (self.pasta_skin / nome_arquivo)  # Une o diretório base da skin com o nome do arquivo desejado
        return arquivo_skin  # Retorna o objeto contendo o endereço completo do arquivo
    
    # ==========================================
    # CARREGAR INI
    # ==========================================
    # Método que analisa as especificações textuais do arquivo de parâmetros da skin
    def carregar_skin_ini(self):
        
        skin_ini = self.obter_arquivo('skin.ini')  # Busca o endereço do arquivo de texto de configuração da skin
        
        parser = configparser.ConfigParser()  # Instancia o interpretador de estruturas .ini do Python
        parser.read(skin_ini, encoding='utf-8')  # Abre e processa o arquivo texto usando a codificação padrão utf-8
        
        # Condicional que valida se a seção obrigatória existe dentro do mapeamento do arquivo lido
        if 'aparência' not in parser:
            return  # Interrompe a execução caso o bloco de dados visuais esteja ausente
        
        seção = parser['aparência']  # Captura o dicionário de chaves pertencentes à seção de aparência
        self.nome = seção.get('Nome', fallback='padrao')  # Extrai o nome da skin ou aplica o valor reserva 'padrao'
        
        self.largura_nota = seção.getint('LarguraNota', fallback=64)  # Lê o tamanho horizontal das notas convertendo para inteiro
        self.altura_nota = seção.getint('AlturaNota', fallback=24)  # Lê o tamanho vertical das notas convertendo para inteiro
        
        self.largura_receptor = seção.getint('LarguraReceptor', fallback=self.largura_nota)  # Configura a largura dos receptores ou espelha a largura da nota
        self.altura_receptor = seção.getint('AlturaReceptor', fallback=self.altura_nota)  # Configura a altura dos receptores ou espelha a altura da nota
    
    # ==========================================
    # CARREGAR TEXTURAS
    # ==========================================
    # Método responsável por varrer o diretório abrindo e formatando cada elemento gráfico
    def carregar_texturas(self):
        
        self.texturas_notas.clear()  # Limpa o vetor de notas para garantir que não haja sobras de memórias passadas
        self.texturas_receptor.clear()  # Limpa o vetor de receptores neutros para iniciar o preenchimento do zero
        self.texturas_receptor_clicado.clear()  # Limpa o vetor de receptores pressionados antes de reinserir os dados
        
        # Laço de repetição que roda quatro vezes para carregar os recursos de cada uma das quatro trilhas do jogo
        for i in range(1, 5):
            
            caminho_nota = (self.obter_arquivo(f'nota_{i}.png'))  # Constrói o nome do arquivo de imagem correspondente à trilha atual
            textura_nota = (arcade.load_texture(caminho_nota))  # Dispara a leitura gráfica do Arcade para decodificar o arquivo PNG
            textura_nota.width = self.largura_nota  # Sobrescreve a largura interna da textura com o valor lido do .ini
            textura_nota.height = self.altura_nota  # Sobrescreve a altura interna da textura com o valor lido do .ini
            self.texturas_notas.append(textura_nota)  # Insere a textura configurada no final do vetor de controle de notas
            
            caminho_receptor = (self.obter_arquivo(f'receptor_{i}.png'))  # Monta o endereço da imagem do botão estático neutro
            textura_receptor = (arcade.load_texture(caminho_receptor))  # Carrega o arquivo visual do botão receptor na memória gráfica
            
            tamanho_quadrado = max(self.largura_receptor, self.altura_receptor)  # Define a dimensão ideal capturando a maior aresta configurada
            textura_receptor.width = tamanho_quadrado  # Força a dimensão de largura a se equiparar ao maior eixo
            textura_receptor.height = tamanho_quadrado  # Força a dimensão de altura a se equiparar ao maior eixo
            self.texturas_receptor.append(textura_receptor)  # Guarda o sprite circular quadrado na lista de receptores padrão
            
            caminho_receptor_clicado = (
                self.obter_arquivo(f'receptor_{i}_hit.png')
            )  # Constrói o caminho para a variante visual do botão sob pressão de clique
            
            # Condicional que checa se o arquivo específico de clique existe fisicamente no disco rígido
            if caminho_receptor_clicado.exists():
                textura_receptor_clicado = (
                    arcade.load_texture(caminho_receptor_clicado)
                )  # Carrega a variação visual de clique da trilha correspondente
                textura_receptor_clicado.width = tamanho_quadrado  # Iguala a largura do botão ativo ao tamanho proporcional padrão
                textura_receptor_clicado.height = tamanho_quadrado  # Iguala a altura do botão ativo ao tamanho proporcional padrão
            
            # Caso a imagem customizada de clique não esteja presente na pasta da skin
            else:
                textura_receptor_clicado = textura_receptor  # Clona a textura neutra como alternativa segura para evitar falhas do motor 2D
            
            self.texturas_receptor_clicado.append(
                textura_receptor_clicado
            )  # Adiciona a textura final no vetor correspondente aos receptores acionados
