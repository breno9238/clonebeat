
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
VOLUME = 0.5


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
VELOCIDADE_QUEDA = 1100

Y_RECEPTOR = 100

MARGEM_ACERTO = 400


# ==========================================
# COLUNAS
# ==========================================

COLUNAS_X = [795, 905, 1015, 1125]


# ==========================================
# INPUTS
# ==========================================

USAR_TECLADO = False

TECLAS_COLUNAS = {
    arcade.key.D: 0,
    arcade.key.F: 1,
    arcade.key.J: 2,
    arcade.key.K: 3
}