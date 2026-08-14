import arcade

from pathlib import Path

# ==========================================
# JANELA
# ==========================================
LARGURA_TELA = 800
ALTURA_TELA = 600

TITULO_JOGO = 'SUPER 4K RHYTHM'

VOLUME = 0.5

# ==========================================
# CAMINHOS
# ==========================================
CAMINHO_PASTA_FASES = Path(r'fases')

# ==========================================
# NOTAS
# ==========================================
VELOCIDADE_QUEDA = 1200

Y_RECEPTOR = 50
MARGEM_ACERTO = 80

# ==========================================
# COLUNAS
# ==========================================
COLUNAS_X = [250, 350, 450, 550]

# ==========================================
# INPUTS
# ==========================================
USAR_TECLADO = True

TECLAS_COLUNAS = {
    arcade.key.A: 0,
    arcade.key.S: 1,
    arcade.key.J: 2,
    arcade.key.K: 3
}