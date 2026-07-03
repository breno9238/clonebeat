import configparser

from pathlib import Path

import arcade


# ==========================================
# GERENCIADOR DE SKINS
# ==========================================
class GerenciadorSkin:

    def __init__(self, pasta_skin):

        self.pasta_skin = Path(pasta_skin)

        # ==========================================
        # SKIN PADRÃO
        # ==========================================
        self.pasta_padrao = Path(
            "recursos/skins/padrao"
        )

        self.data = {}

        self.texturas_notas = []

        self.texturas_receptor = []

        self.carregar_skin_ini()

        self.carregar_texturas()

    # ==========================================
    # RETORNA ARQUIVO
    # ==========================================
    def obter_arquivo(self, nome_arquivo):

        arquivo_skin = (
            self.pasta_skin / nome_arquivo
        )

        # ==========================================
        # USA ARQUIVO DA SKIN
        # ==========================================
        if arquivo_skin.exists():

            return arquivo_skin

        # ==========================================
        # FALLBACK padrao
        # ==========================================
        arquivo_padrao = (
            self.pasta_padrao / nome_arquivo
        )

        return arquivo_padrao

    # ==========================================
    # CARREGAR INI
    # ==========================================
    def carregar_skin_ini(self):

        skin_ini = self.obter_arquivo(
            "skin.ini"
        )

        parser = configparser.ConfigParser()

        parser.read(
            skin_ini,
            encoding="utf-8"
        )

        # ==========================================
        # padraoS
        # ==========================================
        self.data = {

            "nome": "padrao",

            "largura_nota": 64,

            "altura_nota": 24,
        }

        # ==========================================
        # NÃO TEM [SKIN]
        # ==========================================
        if "SKIN" not in parser:

            return

        secao = parser["SKIN"]

        self.data["nome"] = secao.get(
            "Nome",
            fallback="padrao"
        )

        self.data["largura_nota"] = (
            secao.getint(
                "LarguraNota",
                fallback=64
            )
        )

        self.data["altura_nota"] = (
            secao.getint(
                "AlturaNota",
                fallback=24
            )
        )

    # ==========================================
    # CARREGAR TEXTURAS
    # ==========================================
    def carregar_texturas(self):

        self.texturas_notas.clear()

        self.texturas_receptor.clear()

        for i in range(1, 5):

            # ==========================================
            # NOTAS
            # ==========================================
            caminho_nota = (
                self.obter_arquivo(
                    f"note_{i}.png"
                )
            )

            textura_nota = (
                arcade.load_texture(
                    caminho_nota
                )
            )

            self.texturas_notas.append(
                textura_nota
            )

            # ==========================================
            # RECEPTORES
            # ==========================================
            caminho_receptor = (
                self.obter_arquivo(
                    f"receptor_{i}.png"
                )
            )

            textura_receptor = (
                arcade.load_texture(
                    caminho_receptor
                )
            )

            self.texturas_receptor.append(
                textura_receptor
            )