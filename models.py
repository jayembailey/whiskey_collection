from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, unique = True, default = '')
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f'User {self.email} added to database'

class Whiskey(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    year = db.Column(db.String(5), default = '')
    price = db.Column(db.Float, default = '')
    variety = db.Column(db.String(50), default = '')
    date_acquired = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    
    def __init__(self, name, year, price, variety, user_token,):
        self.id = self.set_id()
        self.name = name
        self.year = year
        self.price = price
        self.variety = variety
        self.user_token = user_token

    def set_id(self):
        return secrets.token_urlsafe()

    def __repr__(self):
        return f'{self.name} added to collection'

class WhiskeySchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'year', 'price', 'variety']

whiskey_schema = WhiskeySchema()
whiskeys_schema = WhiskeySchema(many = True)