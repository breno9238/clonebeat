from pathlib import Path

# ==========================================
# GERENCIADOR DE NOTAS
# ==========================================
class GerenciadorNotas:
    
    def __init__(self, arquivo_notas):
        
        self.arquivo_notas = Path(arquivo_notas)
        self.data = self.carregar_notas_ini()
    
    # ==========================================
    # CARREGAR INI
    # ==========================================
    def carregar_notas_ini(self):
        
        notas = []
        
        with open(self.arquivo_notas, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        
        lendo_hitobjects = False
        
        for linha in linhas:
            
            linha = linha.strip()
            
            if linha == '[HitObjects]':
                lendo_hitobjects = True
                continue
            
            if lendo_hitobjects and linha.startswith('['):
                break
            
            if lendo_hitobjects and linha and ',' in linha:
                
                partes   = linha.split(',')
                
                x_osu    = int(partes[0])
                tempo_ms = int(partes[2])
                
                coluna   = min(max(int(x_osu / 128), 0), 3)
                tempo    = tempo_ms / 1000
                
                notas.append((tempo, coluna))
        
        notas.sort(key=lambda n: n[0])
        return notas