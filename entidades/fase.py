import os


# ==========================================
# FASE
# ==========================================
class Fase:

    def __init__(
        self,
        numero_mundo,
        nome,
        notas,
        skin,
        música,
        desbloqueada=True,
        melhor_nota='-'
    ):
        self.numero_mundo = numero_mundo
        self.nome = nome
        self.notas = notas
        self.skin = skin
        self.música = música
        self.desbloqueada = desbloqueada
        self.melhor_nota = melhor_nota