from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
db = SQLAlchemy(app)

class Korisnik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    lozinka = db.Column(db.String(100), nullable=False)

class Predmet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    korisnik_id = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)
    naziv = db.Column(db.String(100), nullable=False)

class Raspored(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    predmet_id = db.Column(db.Integer, db.ForeignKey('predmet.id'), nullable=False)
    ime = db.Column(db.String(100), nullable=False)

class Ocena(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    korisnik_id = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)
    predmet_id = db.Column(db.Integer, db.ForeignKey('predmet.id'), nullable=False)
    ocena = db.Column(db.Integer, nullable=False)

class Podsetnik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    korisnik_id = db.Column(db.Integer, db.ForeignKey('korisnik.id'), nullable=False)
    predmet_id = db.Column(db.Integer, db.ForeignKey('predmet.id'), nullable=False)
    naslov = db.Column(db.String(100), nullable=False)
    opis = db.Column(db.Text, nullable=False)
    datum = db.Column(db.DateTime, nullable=False)

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)