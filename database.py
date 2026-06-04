import sqlite3

DB_NAME = 'astrael_pharma.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            categoria TEXT,
            imagem_url TEXT,
            ativo BOOLEAN NOT NULL DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

def get_all_produtos(somente_ativos=False):
    conn = get_db_connection()
    if somente_ativos:
        produtos = conn.execute('SELECT * FROM produtos WHERE ativo = 1 ORDER BY id DESC').fetchall()
    else:
        produtos = conn.execute('SELECT * FROM produtos ORDER BY id DESC').fetchall()
    conn.close()
    return produtos

def get_produto(produto_id):
    conn = get_db_connection()
    produto = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
    conn.close()
    return produto

def add_produto(nome, descricao, preco, quantidade, categoria, imagem_url, ativo=1):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO produtos (nome, descricao, preco, quantidade, categoria, imagem_url, ativo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, descricao, preco, quantidade, categoria, imagem_url, ativo))
    conn.commit()
    conn.close()

def update_produto(produto_id, nome, descricao, preco, quantidade, categoria, imagem_url, ativo):
    conn = get_db_connection()
    conn.execute('''
        UPDATE produtos
        SET nome = ?, descricao = ?, preco = ?, quantidade = ?, categoria = ?, imagem_url = ?, ativo = ?
        WHERE id = ?
    ''', (nome, descricao, preco, quantidade, categoria, imagem_url, ativo, produto_id))
    conn.commit()
    conn.close()

def delete_produto(produto_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
    conn.commit()
    conn.close()

def toggle_produto_ativo(produto_id):
    conn = get_db_connection()
    produto = conn.execute('SELECT ativo FROM produtos WHERE id = ?', (produto_id,)).fetchone()
    if produto:
        novo_status = 0 if produto['ativo'] else 1
        conn.execute('UPDATE produtos SET ativo = ? WHERE id = ?', (novo_status, produto_id))
        conn.commit()
    conn.close()

def update_estoque(produto_id, quantidade_comprada):
    conn = get_db_connection()
    conn.execute('UPDATE produtos SET quantidade = quantidade - ? WHERE id = ? AND quantidade >= ?', 
                 (quantidade_comprada, produto_id, quantidade_comprada))
    conn.commit()
    conn.close()
