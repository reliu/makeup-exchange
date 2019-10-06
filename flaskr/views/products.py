import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr import models

table_name = "products"
bp = Blueprint(table_name, __name__, url_prefix=f'/{table_name}')


@bp.route('/', methods=['GET'])
def get_all_products():
    if request.method == 'GET':  # FIXME: is "if" redundant?
        connection = models.get_db()
        found_products = connection.execute(
            'SELECT * FROM products;'
        ).fetchall()
        connection.close()
        found_products = [map(str, product) for product in found_products]
        found_products_str = '\n'.join(','.join(product) for product in found_products)
        print("found_products=", found_products_str)
        return found_products_str


@bp.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """return the information for <product_id>"""
    connection = models.get_db()
    found_product = connection.execute(
        'SELECT * FROM %s WHERE id = %s;' %
        (table_name, product_id)
    ).fetchone()
    connection.close()
    found_product_str = ','.join(map(str, found_product))

    print("found_product=", found_product_str)
    return found_product_str


@bp.route('/<product_id>', methods=['POST'])
def post_product(product_id):
    """create information for <product_id>"""
    name = request.json['ProductName']
    description = request.json['ProductDescription']
    price = request.json['ProductPrice']
    seller = request.json['ProductSeller']

    print('INSERT INTO %s (seller_id,id,name,description,price) '
          'VALUES ((SELECT id FROM users WHERE username = \"%s\"),\"%s\",\"%s\",\"%s\",\"%s\");' %
          (table_name, seller, product_id, name, description, price))

    connection = models.get_db()
    connection.execute(
        'INSERT INTO %s (seller_id,id,name,description,price) '
        'VALUES ((SELECT id FROM users WHERE username = \"%s\"),\"%s\",\"%s\",\"%s\",\"%s\");' %
        (table_name, seller, product_id, name, description, price)
    )
    connection.commit()
    connection.close()
    return 'POST product'


@bp.route('/<product_id>', methods=['PATCH'])
def patch_product(product_id):
    name = request.json["ProductName"] if "ProductName" in request.json else None
    description = request.json["ProductDescription"] if "ProductDescription" in request.json else None
    price = request.json["ProductPrice"] if "ProductPrice" in request.json else None
    print(f'name={name}, description={description}, price={price}')

    connection = models.get_db()
    if name:
        models.update_sql_table(connection, table_name, product_id, "name", name)
    if description:
        models.update_sql_table(connection, table_name, product_id, "description", description)
    if price:
        models.update_sql_table(connection, table_name, product_id, "price", price)
    connection.close()
    return 'PATCH product'


@bp.route('/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    """delete product with ID <product_id>"""
    connection = models.get_db()
    connection.execute(
        'DELETE FROM %s WHERE id = %s;' %
        (table_name, product_id)
    )
    connection.commit()
    connection.close()

    return "DELETE product"
