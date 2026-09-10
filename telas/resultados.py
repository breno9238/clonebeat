import arcade

from regras.configuracoes import *


# ==========================================
# RESULTADOS
# ==========================================
class TelaResultados(arcade.View):

    def __init__(
        self,
        pontuacao,
        combo,
        precisao=100.00,
        perfeito=0,
        bom=0,
        falha=0
    ):

        super().__init__()

        self.pontuacao = pontuacao
        self.combo = combo
        self.precisao = precisao
        self.perfeito = perfection = perfeito
        self.bom = bom
        self.falha = falha

    def on_draw(self):

        self.clear()

        arcade.set_background_color(
            (20, 10, 40)
        )

        largura_real = self.window.width
        altura_real = self.window.height
        centro_x = largura_real / 2
        alinhamento_esquerda = centro_x - 250  

        arcade.draw_text(
            'RESULTADO',
            centro_x,
            altura_real * 0.85,
            arcade.color.CYAN,
            65,
            anchor_x='center',
            bold=True
        )

        arcade.draw_text(
            f'PONTUAÇÃO: {self.pontuacao}',
            alinhamento_esquerda,
            altura_real * 0.70,
            arcade.color.WHITE,
            38,
            anchor_x='left',
            bold=True
        )

        arcade.draw_text(
            f'PRECISÃO: {self.precisao:.2f}%',
            alinhamento_esquerda,
            altura_real * 0.62,
            arcade.color.GOLD,
            38,
            anchor_x='left',
            bold=True
        )

        # 🚀 ALTERADO: Removido os parênteses com os termos em inglês
        arcade.draw_text(
            f'PERFEITO: {self.perfeito}',
            alinhamento_esquerda,
            altura_real * 0.52,
            arcade.color.LIGHT_GREEN,
            32,
            anchor_x='left',
            bold=True
        )

        arcade.draw_text(
            f'BOM: {self.bom}',
            alinhamento_esquerda,
            altura_real * 0.44,
            arcade.color.LIGHT_BLUE,
            32,
            anchor_x='left',
            bold=True
        )

        arcade.draw_text(
            f'FALHA: {self.falha}',
            alinhamento_esquerda,
            altura_real * 0.36,
            arcade.color.RED,
            32,
            anchor_x='left',
            bold=True
        )

        arcade.draw_text(
            f'MAX COMBO: {self.combo}',
            alinhamento_esquerda,
            altura_real * 0.28,
            arcade.color.WHITE,
            32,
            anchor_x='left',
            bold=True
        )

        arcade.draw_text(
            'APERTE ESC PARA VOLTAR AO MENU',
            centro_x,
            altura_real * 0.12,
            arcade.color.GRAY,
            24,
            anchor_x='center',
            bold=True
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            from telas.menu_principal import MenuPrincipal
            self.window.show_view(MenuPrincipal())
