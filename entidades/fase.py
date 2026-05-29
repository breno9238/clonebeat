import os


# ==========================================
# FASE
# ==========================================
class Fase:

    def __init__(
        self,
        numero_mundo,
        nome,
        arquivo_osu,
        pasta_skin,
        desbloqueada=True,
        melhor_nota="-"
    ):

        self.numero_mundo = numero_mundo

        self.nome = nome

        self.arquivo_osu = arquivo_osu

        self.pasta_skin = pasta_skin

        self.desbloqueada = desbloqueada

        self.melhor_nota = melhor_nota

    @property
    def dados_notas(self):

        if not os.path.exists(self.arquivo_osu):

            return [
                (1.0, 0),
                (1.4, 1),
                (1.8, 2),
                (2.2, 3),
                (2.6, 0),
                (3.0, 1),
                (3.4, 2),
                (3.8, 3),
            ]

        notas = []

        with open(
            self.arquivo_osu,
            "r",
            encoding="utf-8"
        ) as arquivo:

            linhas = arquivo.readlines()

        lendo_hitobjects = False

        for linha in linhas:

            linha = linha.strip()

            if linha == "[HitObjects]":

                lendo_hitobjects = True
                continue

            if lendo_hitobjects and linha.startswith("["):

                break

            if lendo_hitobjects and linha and "," in linha:

                partes = linha.split(",")

                x_osu = int(partes[0])

                tempo_ms = int(partes[2])

                coluna = min(
                    max(int(x_osu / 128), 0),
                    3
                )

                tempo = tempo_ms / 1000

                notas.append(
                    (tempo, coluna)
                )

        notas.sort(
            key=lambda n: n[0]
        )

        return notas