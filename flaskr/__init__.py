import json
import os

from flask import Flask
from flask import request

db = {}  # product_id to Product()


class Product(object):
    def __init__(self, name="", seller="", price=0.0, description=""):
        self.name = name
        self.seller = seller
        self.price = price
        self.description = description


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/products', methods=['GET'])
    def all_products():
        if request.method == 'GET':  # FIXME: "if" redundant?
            return json.dumps([product.__dict__ for product in db.values()])

    @app.route('/products/<product_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
    def products(product_id):
        if request.method == 'GET':
            """return the information for <product_id>"""
            print db
            return json.dumps(db[product_id].__dict__)

        if request.method == 'POST':  # TODO: PATCH?
            """create information for <product_id>"""
            product = Product()
            product.name = request.json['ProductName']
            product.description = request.json['ProductDescription']
            product.price = request.json['ProductPrice']
            product.seller = request.json['ProductSeller']
            db[product_id] = product
            return 'POST product'

        if request.method == 'PATCH':
            name = request.json["ProductName"]
            description = request.json["ProductDescription"]
            price = request.json["ProductPrice"]
            seller = request.json["ProductSeller"]
            if name:
                db[product_id].name = name
            if description:
                db[product_id].description = description
            if price:
                db[product_id].price = price
            if seller:
                db[product_id].seller = seller
            return 'PATCH product'

        if request.method == 'DELETE':
            """delete product with ID <product_id>"""
            del db[product_id]
            if product_id not in db:
                return "product deleted"
            return "ERROR: product was not deleted"
        else:  # FIXME - do we need this?
            # POST Error 405 Method Not Allowed
            return 'error'

    return app
