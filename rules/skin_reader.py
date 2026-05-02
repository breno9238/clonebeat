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
        
        
        self.parser = parser.ConfigParser()
        
        for zip_file in self.new_skins:
            
            new_skin = zip_file.with_suffix("")
            new_skin.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(zip_file, "r") as zip_osk:
                zip_osk.extractall(new_skin)
            
            zip_file.unlink()
            
        
        for skin in pasta_skins.iterdir():
            
            if skin.is_dir():
                
                skin_obj = SkinExtract(skin, self.skins_list)
                self.skins_list.append(skin_obj)
                # if "preview.json" in skin.exists():
                
                #     with open(skin/"preview.json", "r", encoding="utf-8") as raw_preview:
                #         self.preview = json.load(raw_preview)
                
                # elif "skin.ini" in skin.exists():
                
                #     with open(skin/"skin.ini", "r", encoding="utf-8") as raw_preview:
                #         self.preview = json.load(raw_preview)
                
                #else:
                #    continue
            
            
            

class SkinExtract:
    def __init__(self, path_skins: Path, skins_list: list):
        self.path = path_skins
        self.name = self.path.name
        self.data = {}
        
        type = self.detect_type()
        if type == "osu":
            self.extract_skin_ini()
            self.show_info() #comando usado apenas para printar as informações da skin
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    def detect_type(self):
        types = {
            "json": "apparence_4k.json",
            "osu": "skin.ini"
        }
        
        for skin_type, file in types.items():
            if (self.path / file).exists():
                return skin_type
        return "unknown"
        
    
    def show_info(self):
        print(f"\n=== {self.name} ===")
        for k, v in self.data.items():
            print(f"{k}: {v}")
    
    def extract_skin_ini(self):
        skin_ini = self.path / "skin.ini"
        
        if not skin_ini.exists():
            return
        
        config = parser.ConfigParser(strict=False, comment_prefixes=("//", ";"), delimiters=":")
        config.read(skin_ini, encoding="utf-8")
        
        general = config["General"] if "General" in config else {}
        mania = config["Mania"] if "Mania" in config else {}
        
        self.data["Name"] = general.get("Name", self.name)
        self.data["Author"] = general.get("Author", "unknown")
        self.data["Version"] = general.get("Version", "unknown")
        
        self.data["columns"] = []
        keys = int(mania.get("Keys", "0") or 0)
        
        if keys == 4:
            
            #--- KEYS ---
            self.data["KeyImage0"] = mania.get("KeyImage0")
            self.data["KeyImage1"] = mania.get("KeyImage1")
            self.data["KeyImage2"] = mania.get("KeyImage2")
            self.data["KeyImage3"] = mania.get("KeyImage3")
            
            #--- KEYS PRESSIONADAS ---
            self.data["KeyImage0D"] = mania.get("KeyImage0D")
            self.data["KeyImage1D"] = mania.get("KeyImage1D")
            self.data["KeyImage2D"] = mania.get("KeyImage2D")
            self.data["KeyImage3D"] = mania.get("KeyImage3D")
            
            #--- NOTES ---
            self.data["NoteImage0"] = mania.get("NoteImage0")
            self.data["NoteImage1"] = mania.get("NoteImage1")
            self.data["NoteImage2"] = mania.get("NoteImage2")
            self.data["NoteImage3"] = mania.get("NoteImage3")
            
            #--- LN HEAD ---
            self.data["NoteImage0H"] = mania.get("NoteImage0H")
            self.data["NoteImage1H"] = mania.get("NoteImage1H")
            self.data["NoteImage2H"] = mania.get("NoteImage2H")
            self.data["NoteImage3H"] = mania.get("NoteImage3H")
            
            #--- LN BODY ---
            self.data["NoteImage0L"] = mania.get("NoteImage0L")
            self.data["NoteImage1L"] = mania.get("NoteImage1L")
            self.data["NoteImage2L"] = mania.get("NoteImage2L")
            self.data["NoteImage3L"] = mania.get("NoteImage3L")
            
            #--- LN TAIL ---
            self.data["NoteImage0T"] = mania.get("NoteImage0T")
            self.data["NoteImage1T"] = mania.get("NoteImage1T")
            self.data["NoteImage2T"] = mania.get("NoteImage2T")
            self.data["NoteImage3T"] = mania.get("NoteImage3T")
            
            #for i in range(4): talvez usar dps codigo mais bonito
            #    self.data[f"KeyImage{i}"] = mania.get(f"KeyImage{i}")
            return self.data
            
            
            
            
    
    def convert_skin_ini(self):
        pass






class Extract_OSZ:  # classe possivelmente inutil
    def __init__(self):
        pass

class Extract_MSZ:  # classe possivelmente inutil
    def __init__(self):
        pass




































