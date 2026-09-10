from pathlib import Path  # Importa a biblioteca para manipulação inteligente de caminhos de arquivos


# ==========================================
# FASE
# ==========================================
# Classe que funciona como uma estrutura de dados para armazenar as informações e caminhos de uma fase
class Fase:
    
    # Método construtor que recebe e armazena todos os parâmetros necessários para identificar e carregar a fase
    def __init__(
        self,
        numero_mundo,
        nome,
        notas,
        skin,
        música,
        background,
    ):
        self.numero_mundo = numero_mundo  # Armazena o identificador numérico sequencial da fase ou mundo
        self.nome = nome  # Armazena o nome textual da fase correspondente à pasta
        self.notas = Path(notas)  # Transforma o caminho do arquivo de notas em um objeto Path do sistema
        self.skin = Path(skin)  # Transforma o caminho do pacote visual de skin em um objeto Path do sistema
        self.música = Path(música)  # Transforma o caminho do arquivo de áudio musical em um objeto Path do sistema
        
        # Condicional que verifica se um arquivo de imagem de fundo foi passado para a fase
        if background is not None:
            self.background = Path(background)  # Converte o caminho da imagem de fundo encontrada em um objeto Path
        # Caso a fase não possua nenhuma imagem de fundo customizada
        else:
            self.background = None  # Define o atributo como nulo para usar a cor de preenchimento padrão do jogo
