import arcade  # Importa a biblioteca Arcade para mapear as teclas do teclado
from pathlib import Path  # Importa a biblioteca para manipulação inteligente de caminhos de arquivos

# ==========================================
# JANELA (Forçado bruto para Full HD)
# ==========================================
LARGURA_TELA = 1920  # Define a largura fixa da tela do jogo em pixels
ALTURA_TELA = 1080  # Define a altura fixa da tela do jogo em pixels

TITULO_JOGO = 'DRUM BEAT'  # Define o nome que será exibido no topo da janela do jogo
VOLUME = 0.5  # Define o volume geral do áudio do jogo (50% do máximo)

# ==========================================
# CAMINHOS
# ==========================================
CAMINHO_PASTA_FASES = Path(r'fases')  # Cria o caminho do sistema para a pasta onde ficam as fases

# ==========================================
# NOTAS
# ==========================================
VELOCIDADE_QUEDA = 1500  # Define a velocidade vertical com que as notas descem na tela
Y_RECEPTOR = 100  # Define a posição vertical fixa dos receptores de notas (onde o jogador deve apertar)
MARGEM_ACERTO = 200  # Define a tolerância em pixels para validar se o jogador acertou a nota

# ==========================================
# COLUNAS (Calculadas de forma bruta para o centro de 1920)
# ==========================================
COLUNAS_X = [795, 905, 1015, 1125]  # Define a posição horizontal fixa de cada uma das 4 colunas

# ==========================================
# INPUTS
# ==========================================
USAR_TECLADO = True  # Define se o jogo aceitará comandos vindo do teclado do computador

TECLAS_COLUNAS = {
    arcade.key.A: 0,  # Mapeia a tecla 'A' do teclado para controlar a primeira coluna (índice 0)
    arcade.key.S: 1,  # Mapeia a tecla 'S' do teclado para controlar a segunda coluna (índice 1)
    arcade.key.J: 2,  # Mapeia a tecla 'J' do teclado para controlar a terceira coluna (índice 2)
    arcade.key.K: 3   # Mapeia a tecla 'K' do teclado para controlar a quarta coluna (índice 3)
}

# ==========================================
# VARIÁVEIS DE CONFIGURAÇÃO DESSA TELA
# ==========================================
skin_atual = 'padrao'  # Define a pasta visual estética que será usada para as notas e menus
