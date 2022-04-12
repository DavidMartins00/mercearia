import locale
import random
import shutil
from os.path import join, dirname, realpath
import os

from flask import render_template, Blueprint, request, jsonify, redirect, url_for
from flask_login import current_user

from app import db
from models import Produto, Categoria
from perms import roles

views = Blueprint('views', __name__)


def isadmin():
    if current_user.is_authenticated:
        if current_user.role == 'Admin':
            return True
    else:
        return False


@views.route('/')
def main():  # put application's code here
    return render_template("index.html", name="Teste")


@views.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():  # put application's code here
    if request.method == 'POST':
        txt = request.form['query']
        print(txt)
        if txt == "":
            res = Produto.query.all()
            return jsonify({'htmlresponse': render_template('responsecards.html', res=res, cat=Categoria.query.all(),
                                                            prod=Produto.query.all(), admin=isadmin())})
        else:
            search = "%{}%".format(txt)
            res = Produto.query.filter(Produto.name.like(search)).all()
            return jsonify({'htmlresponse': render_template('responsecards.html', res=res, cat=Categoria.query.all(),
                                                            prod=Produto.query.all(), admin=isadmin())})


@views.route('/produto/info', methods=['GET', 'POST'])
def produtoInfo():
    print("aaaaaa")
    userid = request.form.get('prodid')
    user = Produto.query.get_or_404(userid)
    return jsonify({'htmlresponse': render_template('response.html', produto=user)})


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/produto/add', methods=['GET', 'POST'])
@roles('Admin')
def produtoAdd():
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    size = request.form.get('quantity')
    category = request.form.get('category')
    foto = request.files['image']

    if foto:
        if allowed_file(foto.filename):
            idfoto = str(random.randrange(1, 9223372036854775807))
            fol = join(dirname(realpath(__file__)), 'static/uploads/')
            fol += "/produtos/" + idfoto
            os.mkdir(fol)

            filename = "foto" + "." + "jpg"
            foto.save(os.path.join(fol, filename))

            produto = Produto(name=name, description=description, price=price, size=size, category_id=category,
                              image=idfoto)

            db.session.add(produto)
            db.session.commit()
            return redirect(url_for('views.main'))


@views.route('/produto/edit', methods=['GET', 'POST'])
@roles('Admin')
def produtoEdit():
    print("aaaaaa")
    prodid = request.form.get('prodid')
    produto = Produto.query.get_or_404(prodid)
    print("bbbbbbbbbbbbb")
    return jsonify({'htmlresponse': render_template('responseedit.html', produto=produto, cat=Categoria.query.all())})


@views.route('/produto/edited', methods=['GET', 'POST'])
@roles('Admin')
def produtoEdited():
    id = request.form.get('id')
    produto = Produto.query.get_or_404(id)
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    size = request.form.get('quantity')
    category = request.form.get('category')
    foto = request.files['image']

    if name:
        produto.name = name
    if description:
        produto.description = description
    if price:
        produto.price = price
    if size:
        produto.size = size
    if category:
        produto.category_id = category

    if foto and allowed_file(foto.filename):
        idfoto = str(random.randrange(1, 9223372036854775807))
        fol = join(dirname(realpath(__file__)), 'static/uploads/')
        ofol = fol + "/produtos/" + str(produto.image)
        fol += "/produtos/" + idfoto
        os.mkdir(fol)

        filename = "foto" + "." + "jpg"
        foto.save(os.path.join(fol, filename))
        if os.path.exists(ofol) and produto.image != "0":
            # removing the file using the os.remove() method
            shutil.rmtree(ofol)
        produto.image = idfoto

    db.session.commit()
    return redirect(url_for('views.main'))


@views.route('/produto/delete/<id>', methods=['GET', 'POST'])
@roles('Admin')
def produtoDelete(id):
    produto = Produto.query.get_or_404(id)
    if produto:
        fol = join(dirname(realpath(__file__)), 'static/uploads/')
        ofol = fol + "/produtos/" + str(produto.image)
        if os.path.exists(ofol):
            # removing the file using the os.remove() method
            shutil.rmtree(ofol)
        db.session.delete(produto)
        db.session.commit()
    return redirect(url_for('views.main'))
