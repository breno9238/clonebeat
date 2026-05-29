import arcade

from regras.configuracoes import *


# ==========================================
# RESULTADOS
# ==========================================
class TelaResultados(arcade.View):

    def __init__(
        self,
        pontuacao,
        combo
    ):

        super().__init__()

        self.pontuacao = pontuacao
        self.combo = combo

    def on_draw(self):

        self.clear()

        arcade.set_background_color(
            (10, 10, 20)
        )

        arcade.draw_text(
            "RESULTADO",
            LARGURA_TELA / 2,
            450,
            arcade.color.CYAN,
            40,
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            f"PONTUAÇÃO: {self.pontuacao}",
            LARGURA_TELA / 2,
            320,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )

        arcade.draw_text(
            f"MAX COMBO: {self.combo}",
            LARGURA_TELA / 2,
            270,
            arcade.color.WHITE,
            24,
            anchor_x="center"
        )