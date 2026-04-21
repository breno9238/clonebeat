from pathlib import Path
import zipfile
d = Path(r'C:\Users\ADM\Desktop\clone\assets\skins\bojii 5.9.21 - 467K Mix.osk')
x = d.with_suffix('')
x.mkdir()
with zipfile.ZipFile(d, 'r') as z:
    z.extractall(x)
d.unlink()