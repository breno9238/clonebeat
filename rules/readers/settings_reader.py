import json
from pathlib import Path

def read_settings():
    
    with open('settings.json', 'r', encoding='utf-8') as settings_json:
        
        # extrai o json para um dicionário python
        settings = json.load(settings_json)
    
    for setting in settings.keys():
        if setting == 'skin': settings[setting] = Path(fr'assets/skins/{settings[setting]}').resolve()
    
    return settings

print(read_settings())