import json

from pathlib import Path


# ==========================================
# GERENCIADOR DE RANKING
# ==========================================

# Define o caminho para o arquivo que armazenará os recordes e rankings.
ARQUIVO_SCORES = Path("pontuações.json")


# ==========================================
# CARREGAR RANKING DA FASE
# ==========================================

# Função que busca a lista de todos os scores salvos de uma fase e dificuldade.
def carregar_ranking(nome_fase, dificuldade):

    # Verifica se o arquivo de scores ainda não existe no computador.
    if not ARQUIVO_SCORES.is_file():
        return []

    # Estrutura de tratamento para evitar travamentos caso o JSON esteja corrompido.
    try:

        # Abre o arquivo de registro em modo de leitura com codificação universal.
        with open(ARQUIVO_SCORES, "r", encoding="utf-8") as f:
            dados = json.load(f)

            # Monta uma chave única combinando os dois parâmetros identificadores.
            chave = f"{nome_fase} - {dificuldade}"

            # Retorna a lista de scores ordenada do maior para o menor ou uma lista vazia.
            lista = dados.get(chave, [])
            lista.sort(key=lambda x: x.get("pontuacao", 0), reverse=True)
            return lista

    # Captura qualquer falha interna de leitura ou decodificação.
    except Exception:
        return []


# ==========================================
# CARREGAR MELHOR SCORE (COMPATIBILIDADE)
# ==========================================

# Função que retorna o dicionário completo do melhor resultado para exibição detalhada.
def carregar_melhor_score(nome_fase, dificuldade):

    # Busca a lista completa do ranking passando os parâmetros de forma direta.
    ranking_atual = carregar_ranking(nome_fase, dificuldade)

    # Condicional que checa se existe pelo menos uma pontuação salva no histórico.
    if ranking_atual:
        
        # Como a lista já vem ordenada, o primeiro item (índice 0) contém os melhores dados.
        return ranking_atual[0]

    # Retorna um dicionário com valores zerados e sem nome caso esteja vazio.
    return {"nome": "NENHUM", "pontuacao": 0, "precisao": 0.0}


# ==========================================
# APAGAR HISTÓRICO DE SCORES
# ==========================================

# Função que remove completamente o ranking de uma combinação de fase e dificuldade.
def apagar_ranking_fase(nome_fase, dificuldade):

    # Verifica se o arquivo físico de dados realmente existe no disco.
    if not ARQUIVO_SCORES.is_file():
        return

    # Tenta ler e processar os dados atuais para limpeza.
    try:
        with open(ARQUIVO_SCORES, "r", encoding="utf-8") as f:
            dados = json.load(f)

        # Monta a chave única identificadora.
        chave = f"{nome_fase} - {dificuldade}"

        # Condicional que remove a chave correspondente caso ela exista no dicionário.
        if chave in dados:
            del dados[chave]

            # Reescreve o arquivo limpo de volta para o disco.
            with open(ARQUIVO_SCORES, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4)            
    except Exception:
        pass


# ==========================================
# SALVAR ENTRADA NO RANKING
# ==========================================

# Função que insere uma nova linha de recorde digitada pelo jogador no ranking.
def salvar_no_ranking(nome_fase, dificuldade, nome_jogador, pontuacao, precisao, perfeito, bom, falha):

    dados = {}

    # Verifica se já existe um histórico de scores salvo para ser lido.
    if ARQUIVO_SCORES.is_file():
        try:
            with open(ARQUIVO_SCORES, "r", encoding="utf-8") as f:
                dados = json.load(f)
        except Exception:
            dados = {}

    # Monta a chave combinada que identifica a fase e a dificuldade correspondente.
    chave = f"{nome_fase} - {dificuldade}"

    # Recupera o ranking atual guardado na chave ou inicia uma lista vazia.
    if chave not in dados:
        dados[chave] = []

    # Cria o dicionário com os dados completos alinhados da tentativa do jogador.
    nova_entrada = {
        "nome": nome_jogador.upper().strip() if nome_jogador.strip() else "ANÔNIMO",
        "pontuacao": pontuacao,
        "precisao": round(precisao, 2),
        "perfeito": perfeito,
        "bom": bom,
        "falha": falha
    }

    # Adiciona a nova tentativa ao histórico da fase.
    dados[chave].append(nova_entrada)

    # Ordena a lista de registros para manter o topo com os melhores scores.
    dados[chave].sort(key=lambda x: x["pontuacao"], reverse=True)

    # Mantém apenas os 10 melhores resultados para não sobrecarregar a tela de exibição.
    dados[chave] = dados[chave][:10]

    # Abre o arquivo em modo de escrita para atualizar o documento no disco físico.
    try:
        with open(ARQUIVO_SCORES, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4)
        return True
    except Exception:
        return False
