from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/cad/usuario')
def usuario():
    return render_template('usuario.html', titulo='Cadastro de Usuário')

@app.route('/cad/caduser', methods=['POST'])
def caduser():
    print('usuario cadastrado')
    return request.form

@app.route('/cad/anuncios')
def anuncios():
    return render_template('anuncios.html', titulo='Cadastro de Anúncio')

@app.route('/cad/cadanuncio', methods=['POST'])
def cadanuncio():
    print('anuncio cadastrado')
    return request.form

@app.route('/anuncios/pergunta', methods=['GET', 'POST'])
def pergunta():
    if request.method == 'POST':
        print('pergunta enviada')
        return request.form

    return render_template('pergunta.html')

@app.route('/anuncios/favoritos', methods=['GET', 'POST'])
def favoritos():
    if request.method == 'POST':
        print('favorito inserido')
        return '<h4>Anúncio adicionado aos favoritos</h4>'

    return render_template('favoritos.html')

@app.route('/anuncios/compra', methods=['GET', 'POST'])
def compra():
    if request.method == 'POST':
        print('anuncio comprado')
        return '<h4>Compra realizada com sucesso</h4>'

    return render_template('compra.html')

@app.route('/config/categoria', methods=['GET', 'POST'])
def categoria():
    if request.method == 'POST':
        print('categoria criada')
        return request.form

    return render_template('categoria.html')

@app.route('/relatorios/vendas')
def relatorio_vendas():
    return render_template('relatorio_vendas.html')

@app.route('/relatorios/compras')
def relatorio_compras():
    return render_template('relatorio_compras.html')
