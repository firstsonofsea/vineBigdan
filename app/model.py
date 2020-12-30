from app import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    email = db.Column(db.String(64))
    kol = db.Column(db.Integer)


class Kol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kol_vo = db.Column(db.Integer)
