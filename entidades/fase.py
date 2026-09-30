from pathlib import Path


# ==========================================
# FASE
# ==========================================
# Classe que funciona como uma estrutura de dados para armazenar as informações e caminhos de uma fase.
class Fase:
    
    # Método construtor que recebe e armazena todos os parâmetros necessários para identificar e carregar a fase.
    def __init__(
        self,
        numero_mundo,
        nome,
        pasta_fase,
        skin,
        música,
        fundo,
    ):
        self.numero_mundo = numero_mundo  # Armazena o identificador numérico sequencial da fase ou mundo.
        self.nome = nome  # Armazena o nome textual da fase correspondente à pasta.
        self.pasta_fase = Path(pasta_fase)  # Transforma o caminho do diretório da fase em um objeto Path.
        self.skin = Path(skin)  # Transforma o caminho do pacote visual de skin em um objeto Path do sistema.
        self.música = Path(música)  # Transforma o caminho do arquivo de áudio musical em um objeto Path do sistema.
        
        # Condicional que verifica se um arquivo de imagem de fundo foi passado para a fase.
        if fundo is not None:
            self.fundo = Path(fundo)  # Converte o caminho da imagem de fundo encontrada em um objeto Path.
        # Caso a fase não possua nenhuma imagem de fundo customizada.
        else:
            self.fundo = None  # Define o atributo como nulo para usar a cor de preenchimento padrão do jogo.

        # Lista que armazenará os mapeamentos das dificuldades identificadas na pasta.
        self.lista_dificuldades = []

        # Controla o índice numérico da dificuldade selecionada pelo menu.
        self.indice_dificuldade = 0

        # Percorre sequencialmente todos os itens de dados dentro da pasta específica da fase.
        for arquivo in sorted(self.pasta_fase.iterdir()):
            # Considera e analisa apenas arquivos com a extensão de configuração .ini.
            if arquivo.is_file() and arquivo.suffix == '.ini':
                nome_base = arquivo.stem.upper()
                cor_dificuldade = (255, 255, 0)  # Define a cor amarela padrão como fallback seguro.

                # Condicional que verifica o separador seguro de cor (aceita sublinhado ou barra vertical).
                separador = None
                if '_' in nome_base:
                    separador = '_'
                elif '|' in nome_base:
                    separador = '|'

                # Condicional que processa e extrai o código hexadecimal caso encontre o separador.
                if separador is not None:
                    partes_nome = nome_base.split(separador)
                    nome_limpo = partes_nome[0].strip()
                    hex_cor = partes_nome[1].strip()

                    # Estrutura de tratamento para converter a string hexadecimal em uma tupla RGB válida.
                    try:
                        # Decodifica os pares hexadecimais em canais numéricos inteiros de 0 a 255.
                        r = int(hex_cor[0:2], 16)
                        g = int(hex_cor[2:4], 16)
                        b = int(hex_cor[4:6], 16)
                        cor_dificuldade = (r, g, b)
                    except Exception:
                        nome_limpo = nome_base

                    nome_base = nome_limpo

                # Adiciona o nome limpo, a cor extraída e o endereço absoluto à lista.
                self.lista_dificuldades.append({
                    "nome": nome_base,
                    "cor": cor_dificuldade,
                    "caminho": arquivo
                })

        # Caso nenhum arquivo .ini descritivo seja localizado na varredura.
        if not self.lista_dificuldades:
            # Insere uma configuração reserva apontando para o arquivo notas.ini clássico.
            self.lista_dificuldades.append({
                "nome": "PADRAO",
                "cor": (255, 255, 0),
                "caminho": self.pasta_fase / "notas.ini"
            })

    # ==========================================
    # PROPRIEDADES DINÂMICAS
    # ==========================================

    # Propriedade que retorna o rótulo textual da dificuldade ativada em maiúsculo.
    @property
    def dificuldade_atual(self):
        return self.lista_dificuldades[self.indice_dificuldade]["nome"]

    # Propriedade que retorna a tupla de cor RGB extraída do arquivo de notas ativo.
    @property
    def cor_dificuldade_atual(self):
        return self.lista_dificuldades[self.indice_dificuldade]["cor"]

    # Propriedade que intercepta e injeta dinamicamente o caminho correto do arquivo de notas do jogo.
    @property
    def notas(self):
        return self.lista_dificuldades[self.indice_dificuldade]["caminho"]
