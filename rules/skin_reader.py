#-anotações --------------------------------------------------------------------------

# o nome do .json da skin tem que ser "apparence_4k.json"
# para mudar de skin tenho que trocar o valor do dicionario"settings.json"
# no futuro farzer um código que detecta o tipo de skin, e transformala para .json 
# as skins do osu (.osk) tenho que salvar apenas "4k"(pasta de imagens), "skin.ini" e transformar a parte de 4k do "skin.ini" em .json igual a skin padrão
# no futura juntar as classes (Extract_OSZ) e (Extract_MSZ) e fazer uma classe(ExtractSkin) que detecta automaticamente se a skin é .osz ou .msz

from pathlib import Path
import json
import zipfile
import configparser as parser


class SkinReader:

    def __init__(self):
        
        pasta_skins = Path("skins")
        
        self.new_skins = (
            list(pasta_skins.glob("*.osk")) +
            list(pasta_skins.glob("*.msz"))
        )
        
        self.skins_list:  list = []
        self.extract_osz: list = []
        self.extract_msz: list = []
        
        self.parser = parser.ConfigParser()
        
        for zip_file in self.new_skins:
            
            new_skin = zip_file.with_suffix("")
            new_skin.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(zip_file, "r") as zip_osk:
                zip_osk.extractall(new_skin)
            
            zip_file.unlink()
        
        
        for skin in pasta_skins.iterdir():
            
            if skin.is_dir():
                
                self.skins_list.append(skin)
                # if "preview.json" in skin.exists():
                
                #     with open(skin/"preview.json", "r", encoding="utf-8") as raw_preview:
                #         self.preview = json.load(raw_preview)
                
                # elif "skin.ini" in skin.exists():
                
                #     with open(skin/"skin.ini", "r", encoding="utf-8") as raw_preview:
                #         self.preview = json.load(raw_preview)
                
                #else:
                #    continue
            
            
            

class Skin:
    def __init__(self, path_skins: Path):
        self.path = path_skins
        self.name = self.path.name
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    def detect_type(self):
        types = {
            "json": "apparence_4k.json",
            "osu": "skin.ini"
        }
        
        for skin_type, file in types.items():
            if (self.path / file).exists():
                return skin_type
        return "unknown"
        
    
    
    def load_skin_ini(self):
        
        skin_ini = self.path / "skin.ini"
        
        if not skin_ini.exists():
            return
        
        config = parser.ConfigParser()
        config.read(skin_ini, encoding="utf-8")
        
        self.data = {}
        
        general = config["General"] if "general" in config else {}
        mania = config["Mania"] if "mania" in config else {}
        
        self.data["Name"] = general.get("Name", self.name)
        self.data["Author"] = general.get("Author", "unknown")
        self.data["Version"] = general.get("Version", )
        
        self.data["Keys"] = mania.get("Keys")
        if self.data["Keys"] == "4":
            pass
        
        
    
    def convert_skin_ini(self):
        pass






class Extract_OSZ:  # classe possivelmente inutil
    def __init__(self):
        pass

class Extract_MSZ:  # classe possivelmente inutil
    def __init__(self):
        pass




































