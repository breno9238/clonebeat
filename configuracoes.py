
import arcade
from pathlib import Path


# ==========================================
# JANELA
# ==========================================

LARGURA_TELA = 1920
ALTURA_TELA = 1080

TITULO_JOGO = 'DRUM BEAT'


# ==========================================
# CONFIGURAÇÕES ALTERÁVEIS PELO JOGADOR
# ==========================================

# Volume geral do áudio.
# É alterado pela TelaConfiguracoes.
volume = 0.5


# Skin atualmente selecionada.
# É alterada pela TelaConfiguracoes.
skin_atual = 'padrao'


# ==========================================
# CAMINHOS
# ==========================================

CAMINHO_PASTA_FASES = Path(r'fases')


# ==========================================
# NOTAS
# ==========================================

# Velocidade de queda das notas.
# É alterada pela TelaConfiguracoes.
velocidade_queda = 1100


margem_de_acerto = 400

Y_RECEPTOR = 100

# ==========================================
# COLUNAS
# ==========================================

COLUNAS_X = [795, 905, 1015, 1125]


# ==========================================
# INPUTS
# ==========================================

MODO_INVISIVEL = False  # Controla se as notas ficarão invisíveis na gameplay.

USAR_TECLADO = False

TECLAS_COLUNAS = {
    arcade.key.D: 0,
    arcade.key.F: 1,
    arcade.key.J: 2,
    arcade.key.K: 3
}