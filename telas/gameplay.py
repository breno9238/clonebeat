import arcade

from regras.configuracoes import *

from entidades.nota import Nota

from telas.resultados import TelaResultados

from sistemas.gerenciador_skin import (
    GerenciadorSkin
)


# ==========================================
# GAMEPLAY
# ==========================================
class TelaGameplay(arcade.View):

    def __init__(self, fase, notas):

        super().__init__()

        self.fase = fase

        self.skin = GerenciadorSkin(
            self.fase.pasta_skin
        )

        self.lista_notas = arcade.SpriteList()

        self.notas_restantes = notas

        self.pontuacao = 0

        self.combo = 0
        self.max_combo = 0

        self.resultado = ""

        self.tempo = 0

        self.tempo_spawn = (
            (ALTURA_TELA - Y_RECEPTOR)
            / VELOCIDADE_QUEDA
        )

    def on_update(self, delta_time):

        self.tempo += delta_time

        while (

            self.notas_restantes

            and

            self.tempo >= (
                self.notas_restantes[0][0]
                - self.tempo_spawn
            )
        ):

            tempo_nota, coluna = (
                self.notas_restantes.pop(0)
            )
            print(type(self.skin.texturas_notas[coluna]))
            print(self.skin.texturas_notas[coluna])
            self.lista_notas.append(

                Nota(
                    coluna,

                    ALTURA_TELA,

                    self.skin.texturas_notas[
                        coluna
                    ],

                    self.skin.data[
                        "largura_nota"
                    ],

                    self.skin.data[
                        "altura_nota"
                    ]
                )
            )

        for nota in self.lista_notas:

            nota.atualizar(delta_time)

            if nota.center_y < (
                Y_RECEPTOR - MARGEM_ACERTO
            ):

                nota.remove_from_sprite_lists()

                self.combo = 0

                self.resultado = "MISS"

        if (

            not self.notas_restantes

            and

            len(self.lista_notas) == 0
        ):

            self.window.show_view(

                TelaResultados(
                    self.pontuacao,
                    self.max_combo
                )
            )

    def on_draw(self):

        self.clear()

        arcade.set_background_color(
            arcade.color.BLACK
        )

        for x in COLUNAS_X:

            arcade.draw_lrbt_rectangle_filled(
                x - 35,
                x + 35,
                0,
                ALTURA_TELA,
                (20, 20, 30)
            )

        self.receptores = arcade.SpriteList()

        for i, x in enumerate(COLUNAS_X):
            receptor = arcade.Sprite(self.skin.texturas_receptor[i])
            receptor.center_x = x
            receptor.center_y = Y_RECEPTOR
            self.receptores.append(receptor)
            
            self.receptores.draw()

        self.lista_notas.draw()

        arcade.draw_text(
            f"PONTOS: {self.pontuacao}",
            20,
            560,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            f"COMBO: {self.combo}",
            20,
            530,
            arcade.color.WHITE,
            16
        )

        arcade.draw_text(
            self.resultado,
            LARGURA_TELA / 2,
            350,
            arcade.color.CYAN,
            28,
            anchor_x="center",
            bold=True
        )

    def on_key_press(self, key, modifiers):

        if key not in TECLAS_COLUNAS:
            return

        coluna = TECLAS_COLUNAS[key]

        notas_coluna = [

            n

            for n in self.lista_notas

            if n.coluna == coluna
        ]

        if not notas_coluna:
            return

        nota = min(

            notas_coluna,

            key=lambda n: abs(
                n.center_y - Y_RECEPTOR
            )
        )

        distancia = abs(
            nota.center_y - Y_RECEPTOR
        )

        if distancia <= MARGEM_ACERTO:

            nota.remove_from_sprite_lists()

            self.combo += 1

            self.max_combo = max(
                self.max_combo,
                self.combo
            )

            if distancia <= (
                MARGEM_ACERTO / 2
            ):

                self.pontuacao += 300

                self.resultado = "PERFECT"

            else:

                self.pontuacao += 100

                self.resultado = "GREAT"