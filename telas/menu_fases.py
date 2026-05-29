import arcade

from regras.configuracoes import *

from entidades.fase import Fase

from telas.gameplay import TelaGameplay


# ==========================================
# MENU FASES
# ==========================================
class MenuFases(arcade.View):

    def __init__(self):
        super().__init__()

        self.fases = []

        for i in range(10):

            self.fases.append(

                Fase(
                    f"1-{i + 1}",

                    f"Sintonia Neon {i + 1}",

                    f"recursos/mapas/fase_{i+1}.osu",

                    f"recursos/skins/fase_{i+1}",

                    desbloqueada=True
                )
            )

        self.indice = 0

    def on_draw(self):

        self.clear()

        arcade.set_background_color(
            (25, 10, 45)
        )

        arcade.draw_text(
            "SELECIONE UMA FASE",
            LARGURA_TELA / 2,
            520,
            arcade.color.WHITE,
            26,
            anchor_x="center",
            bold=True
        )

        for i, fase in enumerate(self.fases):

            coluna = i % 5
            linha = i // 5

            x = 170 + (coluna * 110)
            y = 370 - (linha * 120)

            selecionado = (
                i == self.indice
            )

            cor = (
                arcade.color.CYAN
                if selecionado
                else arcade.color.DARK_BLUE
            )

            arcade.draw_lrbt_rectangle_filled(
                x - 45,
                x + 45,
                y - 45,
                y + 45,
                cor
            )

            arcade.draw_text(
                fase.numero_mundo,
                x,
                y,
                arcade.color.WHITE,
                20,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.LEFT and self.indice > 0:
            self.indice -= 1

        elif key == arcade.key.RIGHT and self.indice < 9:
            self.indice += 1

        elif key == arcade.key.UP and self.indice >= 5:
            self.indice -= 5

        elif key == arcade.key.DOWN and self.indice <= 4:
            self.indice += 5

        elif key == arcade.key.ENTER:

            fase = self.fases[self.indice]

            self.window.show_view(

                TelaGameplay(
                    fase,
                    list(fase.dados_notas)
                )
            )