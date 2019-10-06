import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr import models

table_name = "users"
bp = Blueprint('profiles', __name__, url_prefix='/profiles')


@bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """return the information for <user_id>"""
    connection = models.get_db()
    found_user = connection.execute(
        'SELECT * FROM %s WHERE id = %s;' %
        (table_name, user_id)
    ).fetchone()
    connection.close()
    found_user_str = ','.join(map(str, found_user))

    print("found_user=", found_user_str)
    return found_user_str


@bp.route('/<user_id>', methods=['PATCH'])
def patch_user(user_id):
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

    connection = models.get_db()
    if username:
        models.update_sql_table(connection, table_name, user_id, "username", username)
    if email:
        models.update_sql_table(connection, table_name, user_id, "email", email)
    if first_name:
        models.update_sql_table(connection, table_name, user_id, "first_name", first_name)
    if last_name:
        models.update_sql_table(connection, table_name, user_id, "last_name", last_name)
    if address1:
        models.update_sql_table(connection, table_name, user_id, "address1", address1)
    if address2:
        models.update_sql_table(connection, table_name, user_id, "address2", address2)
    if zipcode:
        models.update_sql_table(connection, table_name, user_id, "zipcode", zipcode)
    if city:
        models.update_sql_table(connection, table_name, user_id, "city", city)
    if state:
        models.update_sql_table(connection, table_name, user_id, "state", state)
    if country:
        models.update_sql_table(connection, table_name, user_id, "country", country)
    if phone:
        models.update_sql_table(connection, table_name, user_id, "phone", phone)
    connection.close()
    return 'PATCH user'


@bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """delete user with ID <user_id>"""
    connection = models.get_db()
    connection.execute(
        'DELETE FROM %s WHERE id = %s;' %
        (table_name, user_id)
    )
    connection.commit()
    connection.close()

    return "DELETE user"


@bp.route('/', methods=['POST'])
def post_user():
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

        connection = models.get_db()
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
