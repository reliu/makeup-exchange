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
                'SELECT * FROM products;'
            ).fetchall()
            connection.close()
            found_products = [map(str, product) for product in found_products]
            found_products_str = '\n'.join(','.join(product) for product in found_products)
            print("found_products=", found_products_str)
            return found_products_str

    @app.route('/products/<product_id>', methods=['GET', 'POST', 'PATCH', 'DELETE'])
    def products(product_id):
        table_name = "products"

        if request.method == 'GET':
            """return the information for <product_id>"""
            connection = db.get_db()
            found_product = connection.execute(
                'SELECT * FROM %s WHERE id = %s;' %
                (table_name, product_id)
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

            print('INSERT INTO %s (seller_id,id,name,description,price) '
                  'VALUES ((SELECT id FROM users WHERE username = \"%s\"),\"%s\",\"%s\",\"%s\",\"%s\");' %
                  (table_name, seller, product_id, name, description, price))

            connection = db.get_db()
            connection.execute(
                'INSERT INTO %s (seller_id,id,name,description,price) '
                'VALUES ((SELECT id FROM users WHERE username = \"%s\"),\"%s\",\"%s\",\"%s\",\"%s\");' %
                (table_name, seller, product_id, name, description, price)
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
                update_sql_table(connection, table_name, product_id, "name", name)
            if description:
                update_sql_table(connection, table_name, product_id, "description", description)
            if price:
                update_sql_table(connection, table_name, product_id, "price", price)
            connection.close()
            return 'PATCH product'

        if request.method == 'DELETE':
            """delete product with ID <product_id>"""
            connection = db.get_db()
            connection.execute(
                'DELETE FROM %s WHERE id = %s;' %
                (table_name, product_id)
            )
            connection.commit()
            connection.close()

            return "DELETE product"
        else:  # FIXME - do we need this?
            # POST Error 405 Method Not Allowed
            return 'error'

    @app.route('/profiles/<user_id>', methods=['GET', 'PATCH', 'DELETE'])
    def users(user_id):
        table_name = "users"

        if request.method == 'GET':
            """return the information for <user_id>"""
            connection = db.get_db()
            found_user = connection.execute(
                'SELECT * FROM %s WHERE id = %s;' %
                (table_name, user_id)
            ).fetchone()
            connection.close()
            found_user_str = ','.join(map(str, found_user))

            print("found_user=", found_user_str)
            return found_user_str

        if request.method == 'PATCH':
            username = request.json["User Name"] if "User Name" in request.json else None
            email = request.json["Email"] if "Email" in request.json else None
            first_name = request.json["First Name"] if "First Name" in request.json else None
            last_name = request.json["Last Name"] if "Last Name" in request.json else None
            address1 = request.json["Address 1"] if "Address 1" in request.json else None
            address2 = request.json["Address 2"] if "Address 2" in request.json else None
            zipcode = request.json["Zip Code"] if "Zip Codee" in request.json else None
            city = request.json["City"] if "City" in request.json else None
            state = request.json["State"] if "State" in request.json else None
            country = request.json["Country"] if "Country" in request.json else None
            phone = request.json["Phone Number"] if "Phone Number" in request.json else None

            connection = db.get_db()
            if username:
                update_sql_table(connection, table_name, user_id, "username", username)
            if email:
                update_sql_table(connection, table_name, user_id, "email", email)
            if first_name:
                update_sql_table(connection, table_name, user_id, "first_name", first_name)
            if last_name:
                update_sql_table(connection, table_name, user_id, "last_name", last_name)
            if address1:
                update_sql_table(connection, table_name, user_id, "address1", address1)
            if address2:
                update_sql_table(connection, table_name, user_id, "address2", address2)
            if zipcode:
                update_sql_table(connection, table_name, user_id, "zipcode", zipcode)
            if city:
                update_sql_table(connection, table_name, user_id, "city", city)
            if state:
                update_sql_table(connection, table_name, user_id, "state", state)
            if country:
                update_sql_table(connection, table_name, user_id, "country", country)
            if phone:
                update_sql_table(connection, table_name, user_id, "phone", phone)
            connection.close()
            return 'PATCH user'

        if request.method == 'DELETE':
            """delete user with ID <user_id>"""
            connection = db.get_db()
            connection.execute(
                'DELETE FROM %s WHERE id = %s;' %
                (table_name, user_id)
            )
            connection.commit()
            connection.close()

            return "DELETE user"
        else:  # FIXME - do we need this?
            # POST Error 405 Method Not Allowed
            return 'error'

    @app.route('/profiles', methods=['POST'])
    def profiles():
        table_name = "users"

        if request.method == 'POST':
            """create new user"""
            username = request.json['User Name']
            email = request.json['Email']
            first_name = request.json['First Name']
            last_name = request.json['Last Name']
            address1 = request.json['Address 1']
            address2 = request.json['Address 2']
            zipcode = request.json['Zip Code']
            city = request.json['City']
            state = request.json['State']
            country = request.json['Country']
            phone = request.json['Phone Number']

            connection = db.get_db()
            connection.execute(
                'INSERT INTO %s '
                '(username,email,first_name,last_name,address1,address2,zipcode,city,state,country,phone)'
                'VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\");' %
                (table_name,
                 username, email, first_name, last_name, address1, address2, zipcode, city, state, country, phone)
            )
            connection.commit()
            connection.close()
            return 'POST user'

    def update_sql_table(connection, table_name, id_key, key, value):
        connection.execute(
            'UPDATE %s SET %s = \"%s\" WHERE id = %s;' %
            (table_name, key, value, id_key)
        )
        connection.commit()

    return app
