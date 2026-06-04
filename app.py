import urllib.parse
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
import database

app = Flask(__name__)
app.secret_key = 'astrael_pharma_secret'

# Inicializar o banco de dados
database.init_db()

def seed_db_if_empty():
    produtos = database.get_all_produtos()
    if len(produtos) == 0:
        # Cadastrar produtos fictícios
        database.add_produto("Paracetamol 750mg", "Analgésico e antitérmico indicado para a redução da febre e alívio de dores leves a moderadas.", 8.50, 50, "Analgésicos", "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 1)
        database.add_produto("Dipirona Gotas 500mg/ml", "Alívio rápido e eficaz para dores intensas e controle de febre.", 6.90, 30, "Analgésicos", "https://images.unsplash.com/photo-1585435557343-3b092031a831?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 1)
        database.add_produto("Vitamina C 1g Efervescente", "Suplemento vitamínico para o fortalecimento do sistema imunológico.", 15.00, 20, "Vitaminas", "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80", 1)

seed_db_if_empty()

# --- AUTENTICAÇÃO ---

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Por favor, faça login para acessar o painel administrativo.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Credenciais simples para acesso
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Usuário ou senha incorretos!', 'error')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Você saiu do sistema de forma segura.', 'success')
    return redirect(url_for('login'))

# --- ROTAS PÚBLICAS ---

@app.route('/')
def index():
    produtos = database.get_all_produtos(somente_ativos=True)
    return render_template('index.html', produtos=produtos)

# --- CARRINHO ---

@app.route('/carrinho')
def carrinho():
    if 'carrinho' not in session:
        session['carrinho'] = {}
    
    itens = []
    subtotal = 0
    for produto_id, quantidade_no_carrinho in session['carrinho'].items():
        produto = database.get_produto(int(produto_id))
        if produto:
            valor_item = produto['preco'] * quantidade_no_carrinho
            subtotal += valor_item
            itens.append({
                'produto': produto,
                'quantidade': quantidade_no_carrinho,
                'valor_item': valor_item
            })
    
    valor_frete = 50.00 if subtotal > 0 else 0.00
    total = subtotal + valor_frete
    
    return render_template('carrinho.html', itens=itens, subtotal=subtotal, frete=valor_frete, total=total)

@app.route('/carrinho/add/<int:produto_id>', methods=['POST'])
def add_to_carrinho(produto_id):
    produto = database.get_produto(produto_id)
    if not produto or not produto['ativo']:
        flash('Produto não encontrado ou inativo.', 'error')
        return redirect(url_for('index'))
    
    if produto['quantidade'] <= 0:
        flash('Produto sem estoque disponível.', 'error')
        return redirect(url_for('index'))

    if 'carrinho' not in session:
        session['carrinho'] = {}

    str_id = str(produto_id)
    quantidade_atual = session['carrinho'].get(str_id, 0)
    
    if quantidade_atual + 1 > produto['quantidade']:
        flash('Quantidade solicitada excede o estoque disponível.', 'error')
    else:
        session['carrinho'][str_id] = quantidade_atual + 1
        session.modified = True
        flash('Produto adicionado ao carrinho!', 'success')

    return redirect(url_for('index'))

@app.route('/carrinho/remove/<int:produto_id>')
def remove_from_carrinho(produto_id):
    str_id = str(produto_id)
    if 'carrinho' in session and str_id in session['carrinho']:
        session['carrinho'].pop(str_id)
        session.modified = True
    return redirect(url_for('carrinho'))

@app.route('/carrinho/limpar')
def limpar_carrinho():
    session.pop('carrinho', None)
    return redirect(url_for('carrinho'))

# --- CHECKOUT ---

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'carrinho' not in session or not session['carrinho']:
        return redirect(url_for('index'))
    
    itens = []
    subtotal = 0
    estoque_suficiente = True
    
    for produto_id, qtd in session['carrinho'].items():
        produto = database.get_produto(int(produto_id))
        if produto:
            if qtd > produto['quantidade']:
                estoque_suficiente = False
                flash(f"Estoque insuficiente para o produto {produto['nome']}.", 'error')
            itens.append({'produto': produto, 'quantidade': qtd})
            subtotal += produto['preco'] * qtd

    valor_frete = 50.00 if subtotal > 0 else 0.00
    total = subtotal + valor_frete

    if request.method == 'POST':
        if not estoque_suficiente:
            return redirect(url_for('carrinho'))

        nome = request.form.get('nome')
        telefone = request.form.get('telefone')
        endereco = request.form.get('endereco')
        observacao = request.form.get('observacao', '')

        texto_pedido = f"*Novo Pedido - ASTRAEL PHARMA*\n\n"
        texto_pedido += f"👤 *Cliente:* {nome}\n"
        texto_pedido += f"📞 *Telefone:* {telefone}\n"
        texto_pedido += f"📍 *Endereço:* {endereco}\n\n"
        texto_pedido += "*Resumo da Compra:*\n"

        for item in itens:
            prod = item['produto']
            qtd = item['quantidade']
            database.update_estoque(prod['id'], qtd)
            texto_pedido += f"• {qtd}x {prod['nome']} (R$ {prod['preco']:.2f})\n"

        texto_pedido += f"\n📦 *Subtotal:* R$ {subtotal:.2f}\n"
        texto_pedido += f"🚚 *Frete (Fixo SP):* R$ {valor_frete:.2f}\n"
        texto_pedido += f"💰 *Total a Pagar:* R$ {total:.2f}*\n"
        if observacao:
            texto_pedido += f"📝 *Observação:* {observacao}\n"
            
        texto_pedido += "\n*Pagamento via Pix (Comprovante a enviar).*"
        
        session.pop('carrinho', None)
        
        numero_whatsapp = "5511945433785"
        texto_encoded = urllib.parse.quote(texto_pedido)
        link_whatsapp = f"https://wa.me/{numero_whatsapp}?text={texto_encoded}"
        
        return render_template('checkout.html', itens=itens, subtotal=subtotal, frete=valor_frete, total=total, sucesso=True, link_whatsapp=link_whatsapp)

    return render_template('checkout.html', itens=itens, subtotal=subtotal, frete=valor_frete, total=total, sucesso=False)

# --- ADMIN ---

@app.route('/admin')
@login_required
def admin():
    produtos = database.get_all_produtos()
    total_produtos = len(produtos)
    produtos_ativos = sum(1 for p in produtos if p['ativo'])
    produtos_sem_estoque = sum(1 for p in produtos if p['quantidade'] <= 0)
    valor_estoque = sum(p['preco'] * p['quantidade'] for p in produtos if p['quantidade'] > 0)
    
    return render_template('admin.html', 
                           produtos=produtos, 
                           total_produtos=total_produtos,
                           produtos_ativos=produtos_ativos,
                           produtos_sem_estoque=produtos_sem_estoque,
                           valor_estoque=valor_estoque)

@app.route('/admin/novo', methods=['GET', 'POST'])
@login_required
def novo_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        quantidade = int(request.form.get('quantidade'))
        categoria = request.form.get('categoria')
        imagem_url = request.form.get('imagem_url')
        ativo = 1 if request.form.get('ativo') else 0
        
        database.add_produto(nome, descricao, preco, quantidade, categoria, imagem_url, ativo)
        flash('Produto adicionado com sucesso.', 'success')
        return redirect(url_for('admin'))
        
    return render_template('editar_produto.html', acao='Novo')

@app.route('/admin/editar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    produto = database.get_produto(produto_id)
    if not produto:
        return redirect(url_for('admin'))
        
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        quantidade = int(request.form.get('quantidade'))
        categoria = request.form.get('categoria')
        imagem_url = request.form.get('imagem_url')
        ativo = 1 if request.form.get('ativo') else 0
        
        database.update_produto(produto_id, nome, descricao, preco, quantidade, categoria, imagem_url, ativo)
        flash('Produto atualizado com sucesso.', 'success')
        return redirect(url_for('admin'))
        
    return render_template('editar_produto.html', acao='Editar', produto=produto)

@app.route('/admin/deletar/<int:produto_id>')
@login_required
def deletar_produto(produto_id):
    database.delete_produto(produto_id)
    flash('Produto excluído.', 'success')
    return redirect(url_for('admin'))

@app.route('/admin/toggle/<int:produto_id>')
@login_required
def toggle_produto(produto_id):
    database.toggle_produto_ativo(produto_id)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)