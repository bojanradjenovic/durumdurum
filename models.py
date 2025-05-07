from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
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
