#-anotações --------------------------------------------------------------------------

# o nome do .json da skin tem que ser "apparence_4k.json"
# para mudar de skin tenho que trocar o valor do dicionario"settings.json"
# no futuro farzer um código que detecta o tipo de skin, e transformala para .json 
# as skins do osu (.osk) tenho que salvar apenas "4k"(pasta de imagens), "skin.ini" e transformar a parte de 4k do "skin.ini" em .json igual a skin padrão

from pathlib import Path
import json
import zipfile
class SkinReader:
    def __init__(self):
        
        pasta_skins = Path("skins")
        
        
        for skin in pasta_skins.iterdir():
            if skin.is_dir():
                with open(skin/"preview.json", "r", encoding="utf-8") as raw_preview:
                    
                    self.preview = json.load(raw_preview)
            
            elif skin.suffix == ".osk":
                
                skin_extraida = skin.with_suffix("")
                skin_extraida.mkdir(exist_ok=True)
                
                with zipfile.ZipFile(skin, "r") as zip_osk:
                    zip_osk.extractall(skin_extraida)
                skin.unlink()
            
            elif skin.suffix == ".msz":
                pass

dicionario = SkinReader()


































