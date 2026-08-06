import configparser

from pathlib import Path

import arcade


# ==========================================
# GERENCIADOR DE SKINS
# ==========================================
class GerenciadorSkin:
    
    def __init__(self, pasta_skin):
        
        self.pasta_skin = Path(pasta_skin)
        
        self.texturas_receptor = []
        self.texturas_receptor_clicado = []
        self.texturas_notas    = []
        self.nome              = None
        self.largura_nota      = None
        self.altura_nota       = None
        
    
        self.carregar_skin_ini()
        self.carregar_texturas()
    
    # ==========================================
    # RETORNA ARQUIVO
    # ==========================================
    def obter_arquivo(self, nome_arquivo):
        
        arquivo_skin = (self.pasta_skin / nome_arquivo)
        return arquivo_skin
    
    # ==========================================
    # CARREGAR INI
    # ==========================================
    def carregar_skin_ini(self):
        
        skin_ini = self.obter_arquivo('skin.ini')
        
        parser = configparser.ConfigParser()
        parser.read(skin_ini, encoding='utf-8')
        
        # NÃO TEM [aparência]
        if 'aparência' not in parser:
            return
        
        seção = parser['aparência']
        self.nome         = seção.get('Nome', fallback='padrao')
        self.largura_nota = seção.getint('LarguraNota', fallback=64)
        self.altura_nota  = seção.getint('AlturaNota', fallback=24)
    
    # ==========================================
    # CARREGAR TEXTURAS
    # ==========================================
    def carregar_texturas(self):
        
        self.texturas_notas.clear()
        self.texturas_receptor.clear()
        self.texturas_receptor_clicado.clear()
        
        for i in range(1, 5):
            
            # NOTAS
            caminho_nota = (self.obter_arquivo(f'note_{i}.png'))
            textura_nota = (arcade.load_texture(caminho_nota))
            self.texturas_notas.append(textura_nota)
            
            # RECEPTORES
            caminho_receptor = (self.obter_arquivo(f'receptor_{i}.png'))
            textura_receptor = (arcade.load_texture(caminho_receptor))
            self.texturas_receptor.append(textura_receptor)
            
            # RECEPTORES CLICADOS
            caminho_receptor_clicado = (
                self.obter_arquivo(f'receptor_{i}_hit.png')
            )
            
            if caminho_receptor_clicado.exists():
                textura_receptor_clicado = (
                    arcade.load_texture(caminho_receptor_clicado)
                )
            
            else:
                textura_receptor_clicado = textura_receptor
            
            self.texturas_receptor_clicado.append(
                textura_receptor_clicado
            )