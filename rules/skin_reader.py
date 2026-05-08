from pathlib import Path
import zipfile

class Skin_Reader:
    def __init__(self):
        caminho = Path("assets/skins")
        
        skins_estraidas = []
        skins_zip = list(caminho.glob("*.osk")) + list(caminho.glob("*.msz"))
        
        for i in skins_zip:
            i = Path(i)
            pasta_skin = i.with_suffix('')
            if not pasta_skin:
                pasta_skin.mkdir()
            
            with zipfile.ZipFile(i, "r") as new_skin:
                new_skin.extractall(pasta_skin)
            skins_estraidas.append(new_skin)
            #i.unlink()
            print(new_skin)


s = Skin_Reader()







