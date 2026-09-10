import arcade

from regras.configuracoes import *
from telas.menu_fases import MenuFases
from telas.menu_principal import MenuPrincipal

def main():
    janela = arcade.Window(
        width=LARGURA_TELA,
        height=ALTURA_TELA,
        title=TITULO_JOGO,
        update_rate=1/144,
        draw_rate=1/144,
        fullscreen=True  # Ativa o modo tela cheia bruto
    )
    
    janela.show_view(MenuPrincipal())
    arcade.run()

if __name__ == '__main__':
    main()
