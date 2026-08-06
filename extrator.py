import os
import zipfile

# 1. Pede o caminho do arquivo ao utilizador
caminho_arquivo = input("Introduza o caminho do arquivo do mapa (.osz/.osk): ").strip()

# Remove aspas automáticas do terminal
caminho_arquivo = caminho_arquivo.strip('"').strip("'")

# 2. Validações de segurança
if not os.path.exists(caminho_arquivo):
    print("❌ Erro: O arquivo não foi encontrado.")
elif not caminho_arquivo.lower().endswith(('.osz', '.osk')):
    print("❌ Erro: O arquivo não é um formato válido do osu!")
else:
    diretorio_base = os.path.dirname(caminho_arquivo)
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_pasta_destino = os.path.splitext(nome_arquivo)[0]
    
    pasta_final = os.path.join(diretorio_base, nome_pasta_destino)
    
    try:
        print(f"\n📂 A extrair para: {pasta_final}...")
        
        # 3. Extrai os ficheiros
        with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
            zip_ref.extractall(pasta_final)
            
        print("✅ Extração concluída com sucesso!")
        
        # 4. Elimina o arquivo original de forma segura
        print(f"🗑️ A eliminar o arquivo original: {nome_arquivo}...")
        os.remove(caminho_arquivo)
        print("✅ Arquivo original eliminado!")
        
    except zipfile.BadZipFile:
        print("❌ Erro: Arquivo corrompido. O original NÃO foi eliminado.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}. O original NÃO foi eliminado.")

