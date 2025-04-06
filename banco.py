from conexao import conectar

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        cpf TEXT UNIQUE,
        cidade TEXT
    )
    ''')

    conn.commit()
    conn.close()
