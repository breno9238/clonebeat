import arcade

from regras.configuracoes import *

from telas.menu_principal import MenuPrincipal


# ==========================================
# MAIN
# ==========================================
def main():
    
    janela = arcade.Window(
        LARGURA_TELA,
        ALTURA_TELA,
        TITULO_JOGO
        )
    
    janela.show_view(MenuPrincipal())
    
    arcade.run()


if __name__ == '__main__':
    main()