from pathlib import Path


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
        background,
    ):
        self.numero_mundo = numero_mundo
        self.nome = nome
        self.notas = Path(notas)
        self.skin = Path(skin)
        self.música = Path(música)
        
        if background is not None:
            self.background = Path(background)
        else:
            self.background = None