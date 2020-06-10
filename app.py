from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    mobile_id = db.Column(db.Integer, primary_key=True)
    ram = db.Column(db.Integer)
    storage_size = db.Column(db.Integer)
    cpu_id = db.Column(db.Integer, db.ForeignKey('cpu.cpu_id'))
    ppi = db.Column(db.Integer)
    price_egp = db.Column(db.Integer)
    rank_selfie = db.Column(db.Integer)
    rank_weights_selfie = db.Column(db.Integer)
    rank_maincamera = db.Column(db.Integer)
    rank_weights_main_camera = db.Column(db.Integer)
    battery_endurance_time = db.Column(db.Integer)
    display_protection = db.Column(db.Boolean)
    mobile = db.Column(db.String(70))

    def __init__(self, mobile_id, ram, storage_size,
                 cpu_id, ppi, price_egp,
                 rank_selfie, rank_weights_selfie, rank_maincamera,
                 rank_weights_mani_camera, battery_endurance_time, display_protection, mobile):
        self.ram = ram
        self.storage_size = storage_size
        self.cpu_id = cpu_id
        self.ppi = ppi
        self.price_egp = price_egp
        self.rank_selfie = rank_selfie
        self.rank_weights_selfie = rank_weights_selfie
        self.rank_maincamera = rank_maincamera
        self.rank_weights_mani_camera = rank_weights_mani_camera
        self.battery_endurance_time = battery_endurance_time
        self.display_protection = display_protection
        self.mobile = mobile


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('mobile_id ', 'ram', 'storage_size', 'cpu_id', 'ppi', 'price_egp',
                  'rank_selfie', 'rank_weights_selfie', 'rank_maincamera', 'rank_weights_main_camera',
                  'battery_endurance_time', 'display_protection', 'mobile')


# Init schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


# ennnd modelllllllls __________________________________________________

# Create a Product
@app.route('/product', methods=['GET'])
def add_product():
    ram = request.json['ram']
    storage_size = request.json['storage_size']
    cpu_id = request.json['cpu_id']
    ppi = request.json['ppi']
    price_egp = request.json['price_egp']
    rank_selfie = request.json['rank_selfie']
    rank_weights_selfie = request.json['rank_weights_selfie']
    rank_maincamera = request.json['rank_maincamera']
    rank_weights_main_camera = request.json['rank_weights_main_camera']
    battery_endurance_time = request.json['battery_endurance_time']
    display_protection = request.json['display_protection']
    mobile = request.json['mobile']


    new_product = Product(ram, storage_size, cpu_id, ppi , price_egp,
                  rank_selfie, rank_weights_selfie, rank_maincamera, rank_weights_main_camera,
                  battery_endurance_time, display_protection, mobile)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)


# Get All Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# Get Single Products
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# Update a Product
@app.route('/product/<mobile_id>', methods=['PUT'])
def update_product(mobile_id):
    product = Product.query.get(mobile_id)

    ram = request.json['ram']
    storage_size = request.json['storage_size']
    cpu_id = request.json['cpu_id']
    ppi = request.json['ppi']
    price_egp = request.json['price_egp']
    rank_selfie = request.json['rank_selfie']
    rank_weights_selfie = request.json['rank_weights_selfie']
    rank_maincamera = request.json['rank_maincamera']
    rank_weights_main_camera = request.json['rank_weights_main_camera']
    battery_endurance_time = request.json['battery_endurance_time']
    display_protection = request.json['display_protection']
    mobile = request.json['mobile']

    product.ram = ram
    product.storage_size = storage_size
    product.cpu_id = cpu_id
    product.price_egp = price_egp
    product.rank_selfie = rank_selfie
    product.rank_weights_selfie = rank_weights_selfie
    product.rank_maincamera = rank_maincamera
    product.rank_weights_main_camera = rank_weights_main_camera
    product.battery_endurance_time = battery_endurance_time
    product.display_protection = display_protection
    product.mobile = mobile

    db.session.commit()

    return product_schema.jsonify(product)


# Delete Product
@app.route('/product/<mobile_id>', methods=['DELETE'])
def delete_product(mobile_id):
    product = Product.query.get(mobile_id)
    db.session.delete(product)
    db.session.commit()

    return product_schema.jsonify(product)


# Run Server
if __name__ == '__main__':
    app.run(debug=True)
