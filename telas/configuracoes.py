import arcade

from regras.configuracoes import *


# ==========================================
# CONFIGURAÇÕES
# ==========================================
class TelaConfiguracoes(arcade.View):

    def __init__(self):
        super().__init__()

        self.skins = list(SKINS.keys())

        self.indice = self.skins.index(
            skin_atual
        )

    def on_draw(self):

        self.clear()

        arcade.set_background_color(
            (15, 15, 30)
        )

        arcade.draw_text(
            "CONFIGURAÇÕES",
            LARGURA_TELA / 2,
            500,
            arcade.color.CYAN,
            36,
            anchor_x="center",
            bold=True
        )

        arcade.draw_text(
            "SKIN ATUAL",
            LARGURA_TELA / 2,
            350,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

        arcade.draw_text(
            self.skins[self.indice],
            LARGURA_TELA / 2,
            300,
            arcade.color.YELLOW,
            32,
            anchor_x="center",
            bold=True
        )

    def on_key_press(self, key, modifiers):

        global skin_atual

        if key == arcade.key.LEFT:

            self.indice = (
                self.indice - 1
            ) % len(self.skins)

        elif key == arcade.key.RIGHT:

            self.indice = (
                self.indice + 1
            ) % len(self.skins)

        elif key == arcade.key.ESCAPE:

            skin_atual = self.skins[self.indice]

            from telas.menu_principal import MenuPrincipal

            self.window.show_view(
                MenuPrincipal()
            )