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
        
        # INCLUSÃO DOS ATRIBUTOS DO RECEPTOR
        self.largura_receptor   = None
        self.altura_receptor    = None
        
    
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
        
        # Configurações das Notas que caem do topo
        self.largura_nota = seção.getint('LarguraNota', fallback=64)
        self.altura_nota  = seção.getint('AlturaNota', fallback=24)
        
        # ALTERADO: Novas configurações exclusivas para os Receptores (Tambores) lá embaixo
        self.largura_receptor = seção.getint('LarguraReceptor', fallback=self.largura_nota)
        self.altura_receptor  = seção.getint('AlturaReceptor', fallback=self.altura_nota)
    
    # ==========================================
    # CARREGAR TEXTURAS
    # ==========================================
    def carregar_texturas(self):
        
        self.texturas_notas.clear()
        self.texturas_receptor.clear()
        self.texturas_receptor_clicado.clear()
        
        for i in range(1, 5):
            
            # NOTAS (Aplica o tamanho exclusivo de nota)
            caminho_nota = (self.obter_arquivo(f'note_{i}.png'))
            textura_nota = (arcade.load_texture(caminho_nota))
            textura_nota.width = self.largura_nota
            textura_nota.height = self.altura_nota
            self.texturas_notas.append(textura_nota)
            
            # RECEPTORES (ALTERADO: Aplica o tamanho exclusivo de receptor)
            caminho_receptor = (self.obter_arquivo(f'receptor_{i}.png'))
            textura_receptor = (arcade.load_texture(caminho_receptor))
            textura_receptor.width = self.largura_receptor
            textura_receptor.height = self.altura_receptor
            self.texturas_receptor.append(textura_receptor)
            
            # RECEPTORES CLICADOS
            caminho_receptor_clicado = (
                self.obter_arquivo(f'receptor_{i}_hit.png')
            )
            
            if caminho_receptor_clicado.exists():
                textura_receptor_clicado = (
                    arcade.load_texture(caminho_receptor_clicado)
                )
                # ALTERADO: Aplica o tamanho exclusivo de receptor
                textura_receptor_clicado.width = self.largura_receptor
                textura_receptor_clicado.height = self.altura_receptor
            
            else:
                textura_receptor_clicado = textura_receptor
            
            self.texturas_receptor_clicado.append(
                textura_receptor_clicado
            )
