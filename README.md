# Astrael Pharma

Sistema web de gestão farmacêutica desenvolvido com **Python, Flask e SQLite**, com foco em controle de estoque, catálogo de produtos e painel administrativo.

## Demonstração

### Catálogo de Produtos

![Catálogo](Tela%20do%20catálogo.png)

### Painel Administrativo

![Dashboard](Tela%20do%20dashboard.png)

## Funcionalidades

* Catálogo de produtos com imagem, preço, laboratório e estoque
* Carrinho de compras
* Painel administrativo
* Cadastro de novos produtos
* Edição de produtos
* Ativação e desativação de produtos
* Exclusão de produtos
* Controle de estoque
* Dashboard com métricas gerais

## Tecnologias utilizadas

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript

## Como executar o projeto

Clone o repositório:

```bash
git clone https://github.com/astraelpy/astrael-pharma.git
```

Acesse a pasta:

```bash
cd astrael-pharma
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie o banco de dados:

```bash
python criar_banco.py
```

Execute a aplicação:

```bash
python app.py
```

Acesse no navegador:

```bash
http://127.0.0.1:5000/
```

## Rotas principais

* `/` - Catálogo de produtos
* `/carrinho` - Carrinho de compras
* `/admin` - Painel administrativo

## Objetivo do projeto

Projeto desenvolvido para estudo de desenvolvimento backend com Python, Flask, SQLite, CRUD, gerenciamento de estoque e aplicações web.

## Status

Projeto em desenvolvimento.
