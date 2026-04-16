import json

def read_settings():
    
    def __init__(self):
        
        with open('settings.json', 'r', encoding='utf-8') as settings:
            
            # extrai o json para um dicionário python
            self.setting = json.load(settings)
        
        # guarda cada valor de cada definição do jogador
        self.skin : str = f'skins/{self.setting['skin']}/apparence_4k.json'
        self.speed: int = self.setting['speed']