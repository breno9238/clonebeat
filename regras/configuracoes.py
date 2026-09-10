import arcade
from pathlib import Path

# ==========================================
# JANELA (Forçado bruto para Full HD)
# ==========================================
LARGURA_TELA = 1920
ALTURA_TELA = 1080

TITULO_JOGO = 'DRUM BEAT'
VOLUME = 0.5

# ==========================================
# CAMINHOS
# ==========================================
CAMINHO_PASTA_FASES = Path(r'fases')

# ==========================================
# NOTAS
# ==========================================
VELOCIDADE_QUEDA = 1500
Y_RECEPTOR = 100  
MARGEM_ACERTO = 200

# ==========================================
# COLUNAS (Calculadas de forma bruta para o centro de 1920)
# ==========================================
COLUNAS_X = [795, 905, 1015, 1125]

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

# ==========================================
# VARIÁVEIS DE CONFIGURAÇÃO DESSA TELA
# ==========================================
# 🚀 ADICIONADO: Define qual pasta dentro de skins/ o jogo vai carregar por padrão
skin_atual = 'padrao'
