import sqlite3

def conectar(banco="colecao_jogos.db"):
    # Cria a conexão com o banco de dados SQLite
    conn = sqlite3.connect(banco)
    return conn

def criar_tabela(nome_banco="colecao_jogos.db"):
    # Conecta e cria a tabela 'jogos' caso ela ainda não exista
    conn = conectar(nome_banco)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jogos (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        estudio TEXT NOT NULL,
        ano_lancamento INTEGER NOT NULL,
        status TEXT CHECK (status IN ('Não Jogado', 'Jogando', 'Zerado')) NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def cadastro_jogo(titulo, estudio, ano_lancamento, banco="colecao_jogos.db"):
    # .strip() remove espaços vazios acidentais antes e depois do texto
    titulo_strip = titulo.strip()
    estudio_strip = estudio.strip()
    
    # 1. Validações de regras de negócio
    if titulo_strip == "": 
        return "O título do jogo não pode ficar vazio!"
    elif estudio_strip == "":
        return "Você precisa informar o estúdio desenvolvedor!"
    elif ano_lancamento > 2026:
        return "O ano de lançamento não pode estar no futuro!"   
    else:
        # 2. Se tudo estiver certo, salva no banco com status inicial 'Não Jogado'
        conn = conectar(banco)
        cursor = conn.cursor()
        # O '?' protege o banco contra invasões (SQL Injection)
        cursor.execute("INSERT INTO jogos (titulo, estudio, ano_lancamento, status) VALUES (?, ?, ?, 'Não Jogado')", 
                       (titulo_strip, estudio_strip, ano_lancamento)) 
        conn.commit()
        conn.close()
        return "Jogo cadastrado com sucesso! 🎮"

def delete_jogo(ID, banco="colecao_jogos.db"):
    if ID <= 0:
        return "ID inválido."
    else:
        conn = conectar(banco)
        cursor = conn.cursor()

        # Primeiro, precisamos descobrir qual é o status atual do jogo
        cursor.execute("SELECT status FROM jogos WHERE ID = ?", (ID,))
        resultado = cursor.fetchone()

        if resultado is None:
            return "Jogo não encontrado!"
        
        status = resultado[0] # Extrai o texto limpo da tupla

        # Regra de negócio: Impede deletar se o jogo estiver sendo jogado
        if status == "Jogando":
            conn.close()
            return "Você não pode deletar um jogo que está 'Jogando' no momento!"
        else:
            # Se for 'Não Jogado' ou 'Zerado', pode deletar
            cursor.execute("DELETE FROM jogos WHERE ID = ?", (ID,))
            conn.commit()
            conn.close()
            return "Jogo deletado com sucesso! 🗑️"

def update_status_jogo(ID, status, banco="colecao_jogos.db"):
    if ID <= 0:
        return "ID inválido."
    else:
        conn = conectar(banco)
        cursor = conn.cursor()
        
        # Atualiza a coluna status baseado no ID informado
        cursor.execute("UPDATE jogos SET status = ? WHERE ID = ?", (status, ID))
        rowsaffected = cursor.rowcount
        
        conn.commit()
        conn.close()

        if rowsaffected > 0:
            return "Status do jogo atualizado com sucesso! ✨"
        else:
            return "Nenhum jogo encontrado com este ID."

def get_jogos(banco="colecao_jogos.db"):
    # Busca todos os jogos salvos para exibir no front-end
    conn = conectar(banco)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jogos")
    dados_jogos = cursor.fetchall()
    conn.close()
    return dados_jogos
