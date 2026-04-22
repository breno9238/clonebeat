import configparser
from skin_reader import SkinReader
from pathlib import Path

read = SkinReader()




for skin in read.skins_list:
    
    parser = configparser.ConfigParser(
    strict=False,           # permite duplicatas
    delimiters=(":"),       # ignora comentários
    comment_prefixes=("//", ";") # usa = como separador
    )
    
    skin_ini = skin / "skin.ini"
    if not skin_ini.exists():
        continue
    
    parser.read(skin_ini, encoding="utf-8")
    
    general = parser["General"] if parser.has_section("General") else {}
    titulo_musica = general.get("name", skin.name)
    print(titulo_musica)
    
    autor = parser["General"]["Author"]
    print(autor)
    
    for section in parser.sections():
        print(section)
        
        #for key, value in parser[section].items():
        #    print("  ", key, "=", value)
        
        