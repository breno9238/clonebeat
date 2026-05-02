from pathlib import Path
import configparser as parser


class SkinTester:
    
    def __init__(self, skins_path: Path):
        self.skins_path = skins_path
        self.run()
    
    
    def run(self):
        
        if not self.skins_path.exists():
            print("Pasta skins não encontrada.")
            return
        
        for skin_folder in self.skins_path.iterdir():
            
            if not skin_folder.is_dir():
                continue
            
            skin_ini = skin_folder / "skin.ini"
            
            if not skin_ini.exists():
                continue
            
            print(f"\n===== SKIN: {skin_folder.name} =====")
            
            self.read_skin(skin_folder, skin_ini)
    
    
    def read_skin(self, skin_folder: Path, skin_ini: Path):
        
        # 🔥 LER E LIMPAR O ARQUIVO (remove //)
        with open(skin_ini, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        clean_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith("//") or stripped == "":
                continue
            
            clean_lines.append(line)
        
        
        # 🔹 pegar GENERAL
        config = parser.ConfigParser(strict=False)
        config.read_string("".join(clean_lines))
        
        general = config["General"] if "General" in config else {}
        
        name = general.get("Name", skin_folder.name)
        author = general.get("Author", "unknown")
        version = general.get("Version", "unknown")
        
        print(f"Nome: {name}")
        print(f"Autor: {author}")
        print(f"Versão: {version}")
        
        
        # 🔥 DETECTAR TODOS OS BLOCOS [Mania]
        mania_blocks = []
        current_block = []
        inside_mania = False
        
        for line in clean_lines:
            stripped = line.strip()
            
            if stripped.startswith("[Mania"):
                
                if current_block:
                    mania_blocks.append(current_block)
                    current_block = []
                
                inside_mania = True
            
            if inside_mania:
                current_block.append(line)
        
        if current_block:
            mania_blocks.append(current_block)
        
        
        # 🔥 PROCESSAR BLOCOS
        found_4k = False
        
        for block in mania_blocks:
            
            block_text = "".join(block)
            
            mania_config = parser.ConfigParser(strict=False)
            mania_config.read_string(block_text)
            
            if "Mania" not in mania_config:
                continue
            
            mania = mania_config["Mania"]
            
            keys = int(mania.get("Keys", 0) or 0)
            
            if keys != 4:
                continue
            
            found_4k = True
            
            print(f"\n--- CONFIG 4K ENCONTRADA ---")
            print(f"Keys: {keys}")
            
            
            # 🔥 PRINT ORGANIZADO POR TIPO
            
            print("\n--- KEYS ---")
            for i in range(keys):
                print(f"Key{i}:", mania.get(f"KeyImage{i}"))
            
            print("\n--- KEYS PRESSIONADAS ---")
            for i in range(keys):
                print(f"Key{i}D:", mania.get(f"KeyImage{i}D"))
            
            print("\n--- NOTES ---")
            for i in range(keys):
                print(f"Note{i}:", mania.get(f"NoteImage{i}"))
            
            print("\n--- LN HEAD ---")
            for i in range(keys):
                print(f"Note{i}H:", mania.get(f"NoteImage{i}H"))
            
            print("\n--- LN BODY ---")
            for i in range(keys):
                print(f"Note{i}L:", mania.get(f"NoteImage{i}L"))
            
            print("\n--- LN TAIL ---")
            for i in range(keys):
                print(f"Note{i}T:", mania.get(f"NoteImage{i}T"))
        
        
        if not found_4k:
            print("Não encontrou configuração 4K nessa skin.")


# 🔥 EXECUÇÃO AUTOMÁTICA
SkinTester(Path("skins"))