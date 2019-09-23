import json
import os

from flask import Flask
from flask import request

from . import db


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

    # initialize database
    db.init_app(app)

    @app.route('/products', methods=['GET'])
    def all_products():
        if request.method == 'GET':  # FIXME: is "if" redundant?
            connection = db.get_db()
            found_products = connection.execute(
                'SELECT * FROM product;'
            ).fetchall()
            connection.close()
            found_products = [map(str, product) for product in found_products]
            found_products_str = '\n'.join(','.join(product) for product in found_products)
            print("found_products=", found_products_str)
            return found_products_str

    @app.route('/products/<product_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
    def products(product_id):
        if request.method == 'GET':
            """return the information for <product_id>"""
            connection = db.get_db()
            found_product = connection.execute(
                'SELECT * FROM product WHERE id = (?);',
                (product_id,)
            ).fetchone()
            connection.close()
            found_product_str = ','.join(map(str, found_product))

            print("found_product=", found_product_str)
            return found_product_str

        if request.method == 'POST':
            """create information for <product_id>"""
            name = request.json['ProductName']
            description = request.json['ProductDescription']
            price = request.json['ProductPrice']
            seller = request.json['ProductSeller']

            connection = db.get_db()
            connection.execute(
                'INSERT INTO user (username) VALUES (?);',
                (seller,)
            )
            connection.execute(
                'INSERT INTO product (seller_id,id,name,description,price) '
                'VALUES ((SELECT id FROM user WHERE username = ?),?,?,?,?);',
                (seller, product_id, name, description, price)
            )
            connection.commit()
            connection.close()
            return 'POST product'

        if request.method == 'PATCH':
            name = request.json["ProductName"] if "ProductName" in request.json else None
            description = request.json["ProductDescription"] if "ProductDescription" in request.json else None
            price = request.json["ProductPrice"] if "ProductPrice" in request.json else None
            print(f'name={name}, description={description}, price={price}')

            connection = db.get_db()
            if name:
                connection.execute(
                    'UPDATE product SET name = ? WHERE id = ?;',
                    (name, product_id)
                )
            if description:
                connection.execute(
                    'UPDATE product SET description = (?) WHERE id = (?);',
                    (description, product_id)
                )
            if price:
                connection.execute(
                    'UPDATE product SET price = (?) WHERE id = (?);',
                    (price, product_id)
                )
            connection.commit()
            connection.close()
            return 'PATCH product'

        if request.method == 'DELETE':
            """delete product with ID <product_id>"""
            connection = db.get_db()
            connection.execute(
                'DELETE FROM product WHERE id = (?);',
                (product_id,)
            )
            connection.commit()
            connection.close()

            return "DELETE product"
        else:  # FIXME - do we need this?
            # POST Error 405 Method Not Allowed
            return 'error'

    return app
