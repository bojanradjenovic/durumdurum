from flask import request, jsonify
from models import db, Korisnik
import bcrypt
import jwt
import datetime
from functools import wraps
from flask_limiter.util import get_remote_address

def init_auth(app, limiter):
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].replace('Bearer ', '')
            if not token:
                return jsonify({'message': 'Token je potreban!'}), 401
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                current_user = Korisnik.query.filter_by(id=data['user_id']).first()
                if not current_user:
                    return jsonify({'message': 'Korisnik ne postoji!'}), 401
            except:
                return jsonify({'message': 'Token je nevažeći!'}), 401
            return f(current_user, *args, **kwargs)
        return decorated

    @app.route('/registruj-se', methods=['POST'])
    @limiter.limit("5 per minute")
    def registruj_se():
        data = request.get_json()
        if Korisnik.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email već postoji!'}), 400
        if len(data['lozinka']) < 6:
            return jsonify({'message': 'Lozinka mora imati najmanje 6 karaktera!'}), 400
        if not any(char.isdigit() for char in data['lozinka']):
            return jsonify({'message': 'Lozinka mora sadržati barem jedan broj!'}), 400
        if not any(char.isalpha() for char in data['lozinka']):
            return jsonify({'message': 'Lozinka mora sadržati barem jedno slovo!'}), 400
        if not any(char in '!@#$%^&*()_+' for char in data['lozinka']):
            return jsonify({'message': 'Lozinka mora sadržati barem jedan specijalni karakter!'}), 400
        hashed_lozinka = bcrypt.hashpw(data['lozinka'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8') 
        novi_korisnik = Korisnik(
            ime=data['ime'],
            prezime=data['prezime'],
            email=data['email'],
            lozinka=hashed_lozinka
        )
        db.session.add(novi_korisnik)
        db.session.commit()
        return jsonify({'message': 'Korisnik registrovan!'}), 201

    @app.route('/login', methods=['POST'])
    @limiter.limit("5 per minute", key_func=lambda: request.get_json().get('email', get_remote_address()))
    def login():
        data = request.get_json()
        korisnik = Korisnik.query.filter_by(email=data['email']).first()
        if not korisnik:
            return jsonify({'message': 'Pogrešan email ili lozinka!'}), 401
        if not bcrypt.checkpw(data['lozinka'].encode('utf-8'), korisnik.lozinka.encode('utf-8')):
            return jsonify({'message': 'Pogrešan email ili lozinka!'}), 401
        
        token = jwt.encode({
            'user_id': korisnik.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({
            'message': 'Uspešno ulogovan!',
            'token': token,
            'user': {'id': korisnik.id, 'ime': korisnik.ime, 'prezime': korisnik.prezime, 'email': korisnik.email}
        }), 200

    @app.route('/logout', methods=['POST'])
    @token_required
    def logout(current_user):
        return jsonify({'message': 'Uspešno izlogovan!'}), 200