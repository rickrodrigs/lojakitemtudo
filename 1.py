from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# ==========================================================
# CONFIGURAÇÃO DO BANCO DE DADOS
# ==========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://pauloteste:paulo200@localhost/lojakitemtudo"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ==========================================================
# MODELS
# ==========================================================

class Usuario(db.Model):
    id = db.Column('usu_id', db.Integer, primary_key=True)
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    senha = db.Column('usu_senha', db.String(256))
    end = db.Column('usu_end', db.String(256))


class Categoria(db.Model):
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))


class Anuncio(db.Model):
    id = db.Column('anu_id', db.Integer, primary_key=True)
    titulo = db.Column('anu_titulo', db.String(256))
    descricao = db.Column('anu_descricao', db.String(500))
    preco = db.Column('anu_preco', db.Float)

    usuario_id = db.Column(
        'usu_id',
        db.Integer,
        db.ForeignKey('usuario.usu_id'),
        nullable=False
    )

    categoria_id = db.Column(
        'cat_id',
        db.Integer,
        db.ForeignKey('categoria.cat_id'),
        nullable=False
    )


class Pergunta(db.Model):
    id = db.Column('per_id', db.Integer, primary_key=True)
    texto = db.Column('per_texto', db.String(500))
    resposta = db.Column('per_resposta', db.String(500))

    usuario_id = db.Column(
        'usu_id',
        db.Integer,
        db.ForeignKey('usuario.usu_id'),
        nullable=False
    )

    anuncio_id = db.Column(
        'anu_id',
        db.Integer,
        db.ForeignKey('anuncio.anu_id'),
        nullable=False
    )


class Compra(db.Model):
    id = db.Column('com_id', db.Integer, primary_key=True)

    quantidade = db.Column('com_quantidade', db.Integer)
    valor = db.Column('com_valor', db.Float)

    usuario_id = db.Column(
        'usu_id',
        db.Integer,
        db.ForeignKey('usuario.usu_id'),
        nullable=False
    )

    anuncio_id = db.Column(
        'anu_id',
        db.Integer,
        db.ForeignKey('anuncio.anu_id'),
        nullable=False
    )


class Favorito(db.Model):
    id = db.Column('fav_id', db.Integer, primary_key=True)

    usuario_id = db.Column(
        'usu_id',
        db.Integer,
        db.ForeignKey('usuario.usu_id'),
        nullable=False
    )

    anuncio_id = db.Column(
        'anu_id',
        db.Integer,
        db.ForeignKey('anuncio.anu_id'),
        nullable=False
    )


# ==========================================================
# CRIAÇÃO DAS TABELAS
# ==========================================================

with app.app_context():
    db.create_all()


# ==========================================================
# TRATAMENTO DE ERRO 404
# ==========================================================

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


# ==========================================================
# INÍCIO
# ==========================================================

@app.route('/')
def index():
    return render_template('base.html')


# ==========================================================
# USUÁRIO - CRUD
# ==========================================================

# READ / LISTAR
@app.route('/cad/usuario')
def usuario():
    usuarios = Usuario.query.all()

    return render_template(
        'usuario.html',
        usuarios=usuarios,
        titulo='Cadastro de Usuário'
    )


# CREATE / CADASTRAR
@app.route('/cad/caduser', methods=['POST'])
def caduser():

    usuario = Usuario(
        nome=request.form.get('user'),
        email=request.form.get('email'),
        senha=request.form.get('senha'),
        end=request.form.get('end')
    )

    db.session.add(usuario)
    db.session.commit()

    print('usuario cadastrado')

    return redirect(url_for('usuario'))


# READ / DETALHAR
@app.route('/usuario/detalhar', methods=['GET', 'POST'])
def buscausuario():

    usuario = None

    if request.method == 'POST':

        id = request.form.get('id')
        usuario = Usuario.query.get(id)

        if not usuario:
            return '<h4>Usuário não encontrado</h4>'

    return render_template(
        'detalhes_usuario.html',
        usuario=usuario
    )


# UPDATE / EDITAR
@app.route('/usuario/editar/<int:id>', methods=['GET', 'POST'])
def editarusuario(id):

    usuario = Usuario.query.get(id)

    if not usuario:
        return '<h4>Usuário não encontrado</h4>'

    if request.method == 'POST':

        usuario.nome = request.form.get('user')
        usuario.email = request.form.get('email')
        usuario.senha = request.form.get('senha')
        usuario.end = request.form.get('end')

        db.session.commit()

        print('usuario editado')

        return redirect(url_for('usuario'))

    return render_template(
        'editar_usuario.html',
        usuario=usuario
    )


# DELETE / EXCLUIR
@app.route('/usuario/deletar/<int:id>', methods=['POST'])
def deletarusuario(id):

    usuario = Usuario.query.get(id)

    if usuario:

        db.session.delete(usuario)
        db.session.commit()

        print('usuario deletado')

    return redirect(url_for('usuario'))


# ==========================================================
# CATEGORIA - CRUD
# ==========================================================

# CREATE / READ
@app.route('/config/categoria', methods=['GET', 'POST'])
def categoria():

    if request.method == 'POST':

        nova_categoria = Categoria(
            nome=request.form.get('nome')
        )

        db.session.add(nova_categoria)
        db.session.commit()

        print('categoria criada')

        return redirect(url_for('categoria'))

    categorias = Categoria.query.all()

    return render_template(
        'categoria.html',
        categorias=categorias
    )


# UPDATE
@app.route('/categoria/editar/<int:id>', methods=['GET', 'POST'])
def editar_categoria(id):

    categoria = Categoria.query.get(id)

    if not categoria:
        return '<h4>Categoria não encontrada</h4>'

    if request.method == 'POST':

        categoria.nome = request.form.get('nome')

        db.session.commit()

        print('categoria editada')

        return redirect(url_for('categoria'))

    return render_template(
        'editar_categoria.html',
        categoria=categoria
    )


# DELETE
@app.route('/categoria/deletar/<int:id>', methods=['POST'])
def deletar_categoria(id):

    categoria = Categoria.query.get(id)

    if categoria:

        db.session.delete(categoria)
        db.session.commit()

        print('categoria deletada')

    return redirect(url_for('categoria'))


# ==========================================================
# ANÚNCIO - CRUD
# ==========================================================

# CREATE / READ
@app.route('/cad/anuncios', methods=['GET', 'POST'])
def anuncios():

    if request.method == 'POST':

        anuncio = Anuncio(
            titulo=request.form.get('titulo'),
            descricao=request.form.get('descricao'),
            preco=request.form.get('preco'),
            usuario_id=request.form.get('usuario_id'),
            categoria_id=request.form.get('categoria_id')
        )

        db.session.add(anuncio)
        db.session.commit()

        print('anuncio cadastrado')

        return redirect(url_for('anuncios'))

    anuncios = Anuncio.query.all()
    usuarios = Usuario.query.all()
    categorias = Categoria.query.all()

    return render_template(
        'anuncios.html',
        anuncios=anuncios,
        usuarios=usuarios,
        categorias=categorias,
        titulo='Cadastro de Anúncio'
    )


# UPDATE
@app.route('/anuncio/editar/<int:id>', methods=['GET', 'POST'])
def editar_anuncio(id):

    anuncio = Anuncio.query.get(id)

    if not anuncio:
        return '<h4>Anúncio não encontrado</h4>'

    if request.method == 'POST':

        anuncio.titulo = request.form.get('titulo')
        anuncio.descricao = request.form.get('descricao')
        anuncio.preco = request.form.get('preco')
        anuncio.usuario_id = request.form.get('usuario_id')
        anuncio.categoria_id = request.form.get('categoria_id')

        db.session.commit()

        print('anuncio editado')

        return redirect(url_for('anuncios'))

    usuarios = Usuario.query.all()
    categorias = Categoria.query.all()

    return render_template(
        'editar_anuncio.html',
        anuncio=anuncio,
        usuarios=usuarios,
        categorias=categorias
    )


# DELETE
@app.route('/anuncio/deletar/<int:id>', methods=['POST'])
def deletar_anuncio(id):

    anuncio = Anuncio.query.get(id)

    if anuncio:

        db.session.delete(anuncio)
        db.session.commit()

        print('anuncio deletado')

    return redirect(url_for('anuncios'))


# ==========================================================
# PERGUNTA - CRUD
# ==========================================================

# CREATE / READ
@app.route('/anuncios/pergunta', methods=['GET', 'POST'])
def pergunta():

    if request.method == 'POST':

        nova_pergunta = Pergunta(
            texto=request.form.get('texto'),
            resposta=request.form.get('resposta'),
            usuario_id=request.form.get('usuario_id'),
            anuncio_id=request.form.get('anuncio_id')
        )

        db.session.add(nova_pergunta)
        db.session.commit()

        print('pergunta cadastrada')

        return redirect(url_for('pergunta'))

    perguntas = Pergunta.query.all()
    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()

    return render_template(
        'pergunta.html',
        perguntas=perguntas,
        usuarios=usuarios,
        anuncios=anuncios
    )


# UPDATE
@app.route('/pergunta/editar/<int:id>', methods=['GET', 'POST'])
def editar_pergunta(id):

    pergunta = Pergunta.query.get(id)

    if not pergunta:
        return '<h4>Pergunta não encontrada</h4>'

    if request.method == 'POST':

        pergunta.texto = request.form.get('texto')
        pergunta.resposta = request.form.get('resposta')
        pergunta.usuario_id = request.form.get('usuario_id')
        pergunta.anuncio_id = request.form.get('anuncio_id')

        db.session.commit()

        print('pergunta editada')

        return redirect(url_for('pergunta'))

    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()

    return render_template(
        'editar_pergunta.html',
        pergunta=pergunta,
        usuarios=usuarios,
        anuncios=anuncios
    )


# DELETE
@app.route('/pergunta/deletar/<int:id>', methods=['POST'])
def deletar_pergunta(id):

    pergunta = Pergunta.query.get(id)

    if pergunta:

        db.session.delete(pergunta)
        db.session.commit()

        print('pergunta deletada')

    return redirect(url_for('pergunta'))


# ==========================================================
# COMPRA - CRUD
# ==========================================================

# CREATE / READ
@app.route('/anuncios/compra', methods=['GET', 'POST'])
def compra():

    if request.method == 'POST':

        nova_compra = Compra(
            quantidade=request.form.get('quantidade'),
            valor=request.form.get('valor'),
            usuario_id=request.form.get('usuario_id'),
            anuncio_id=request.form.get('anuncio_id')
        )

        db.session.add(nova_compra)
        db.session.commit()

        print('compra cadastrada')

        return redirect(url_for('compra'))

    compras = Compra.query.all()
    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()

    return render_template(
        'compra.html',
        compras=compras,
        usuarios=usuarios,
        anuncios=anuncios
    )


# UPDATE
@app.route('/compra/editar/<int:id>', methods=['GET', 'POST'])
def editar_compra(id):

    compra = Compra.query.get(id)

    if not compra:
        return '<h4>Compra não encontrada</h4>'

    if request.method == 'POST':

        compra.quantidade = request.form.get('quantidade')
        compra.valor = request.form.get('valor')
        compra.usuario_id = request.form.get('usuario_id')
        compra.anuncio_id = request.form.get('anuncio_id')

        db.session.commit()

        print('compra editada')

        return redirect(url_for('compra'))

    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()

    return render_template(
        'editar_compra.html',
        compra=compra,
        usuarios=usuarios,
        anuncios=anuncios
    )


# DELETE
@app.route('/compra/deletar/<int:id>', methods=['POST'])
def deletar_compra(id):

    compra = Compra.query.get(id)

    if compra:

        db.session.delete(compra)
        db.session.commit()

        print('compra deletada')

    return redirect(url_for('compra'))


# ==========================================================
# FAVORITO - CRUD
# ==========================================================

# CREATE / READ
@app.route('/anuncios/favoritos', methods=['GET', 'POST'])
def favoritos():

    if request.method == 'POST':

        novo_favorito = Favorito(
            usuario_id=request.form.get('usuario_id'),
            anuncio_id=request.form.get('anuncio_id')
        )

        db.session.add(novo_favorito)
        db.session.commit()

        print('favorito cadastrado')

        return redirect(url_for('favoritos'))

    favoritos = Favorito.query.all()
    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()

    return render_template(
        'favoritos.html',
        favoritos=favoritos,
        usuarios=usuarios,
        anuncios=anuncios
    )


# UPDATE
@app.route('/favorito/editar/<int:id>', methods=['GET', 'POST'])
def editar_favorito(id):

    favorito = Favorito.query.get(id)

    if not favorito:
        return '<h4>Favorito não encontrado</h4>'

    if request.method == 'POST':

        favorito.usuario_id = request.form.get('usuario_id')
        favorito.anuncio_id = request.form.get('anuncio_id')

        db.session.commit()

        print('favorito editado')

        return redirect(url_for('favoritos'))

    usuarios = Usuario.query.all()
    anuncios = Anuncio.query.all()

    return render_template(
        'editar_favorito.html',
        favorito=favorito,
        usuarios=usuarios,
        anuncios=anuncios
    )


# DELETE
@app.route('/favorito/deletar/<int:id>', methods=['POST'])
def deletar_favorito(id):

    favorito = Favorito.query.get(id)

    if favorito:

        db.session.delete(favorito)
        db.session.commit()

        print('favorito deletado')

    return redirect(url_for('favoritos'))


# ==========================================================
# RELATÓRIOS
# ==========================================================

@app.route('/relatorios/vendas')
def relatorio_vendas():
    return render_template('relatorio_vendas.html')


@app.route('/relatorios/compras')
def relatorio_compras():
    return render_template('relatorio_compras.html')
