import configparser

from pathlib import Path

import arcade


# ==========================================
# GERENCIADOR DE SKINS
# ==========================================
class GerenciadorSkin:
    
    def __init__(self, pasta_skin):
        
        self.pasta_skin = Path(pasta_skin)
        
        self.data = {
            'texturas_notas'    : [],
            'texturas_receptor' : [],
            'configurações'     : {}
            }
        
        
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
        self.data['nome']         = seção.get('Nome', fallback='padrao')
        self.data['largura_nota'] = seção.getint('LarguraNota', fallback=64)
        self.data['altura_nota']  = seção.getint('AlturaNota', fallback=24)
    
    # ==========================================
    # CARREGAR TEXTURAS
    # ==========================================
    def carregar_texturas(self):
        
        self.data['texturas_notas'].clear()
        self.data['texturas_receptor'].clear()
        
        for i in range(1, 5):
            
            # NOTAS
            caminho_nota = (self.obter_arquivo(f'note_{i}.png'))
            textura_nota = (arcade.load_texture(caminho_nota))
            self.data['texturas_notas'].append(textura_nota)
            
            # RECEPTORES
            caminho_receptor = (self.obter_arquivo(f'receptor_{i}.png'))
            textura_receptor = (arcade.load_texture(caminho_receptor))
            self.data['texturas_receptor'].append(textura_receptor)