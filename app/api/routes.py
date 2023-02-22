from flask import Blueprint, request, jsonify, render_template, json
from helpers import token_required
from models import db, User, Whiskey, whiskey_schema, whiskeys_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
def get_data():
    return jsonify({'message':'it works!'})

@api.route('/collection', methods = ['POST'])
@token_required
def make_whiskey(current_user_token):
    name = request.json['name']
    year = request.json['year']
    price = request.json['price']
    variety = request.json['variety']
    user_token = current_user_token.token

    print(f'CREATE TESTER: {price}')

    whiskey = Whiskey(name, year, price, variety, user_token)
    
    db.session.add(whiskey)
    db.session.commit()

    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/collection', methods = ['GET'])
@token_required
def get_whiskey(current_user_token):
    a_user = current_user_token.token
    whiskeys = Whiskey.query.filter_by(user_token = a_user)
    response = whiskeys_schema.dump(whiskeys)
    return jsonify(response)

@api.route('/collection/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/collection/<id>', methods = ['PUT', 'POST'])
@token_required
def update_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    whiskey.name = request.json['name']
    whiskey.year = request.json['year']
    whiskey.price = request.json['price']
    whiskey.variety = request.json['variety']
    whiskey.user_token = current_user_token.token

    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('collection/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(curren_user_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = whiskey_schema.dump(whiskey)
    return jsonify(response)