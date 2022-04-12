from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String(150))
    role = db.Column(db.String(150))


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150))
    price = db.Column(db.Float)
    image = db.Column(db.String(150))
    size = db.Column(db.String(150))
    category_id = db.Column(db.Integer, db.ForeignKey('categoria.id'))


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    produto = db.relationship('Produto', backref=db.backref('categoria', lazy=True))
