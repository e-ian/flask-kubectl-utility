import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

# instance of flask app
app = Flask(__name__)
mysql = MySQL()


# MySQL database configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('db_root_password')
app.config['MYSQL_DATABASE_DB'] = os.getenv('db_name')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_SERVICE_HOST')
app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('MYSQL_SERVICE_PORT'))
mysql.init_app(app)


@app.route('/')
def index():
    return 'Welcome to my Flask Api'


@app.route('/create', methods=['POST'])
def add_user():
    """
    Function to create and write user to the MySQL database
    :return: success message, status code
    """

    json = request.json
    name = json['name']
    email = json['email']
    password = json['password']

    if name and email and password and request.method == 'POST':
        sql = "INSERT INTO users(user_name, user_email, user_password) VALUES (%s, %s, %s)"
        data = (name, email, password)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify('User created successfully!')
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify('Please provide name, email and password')


@app.route('/users', methods=['GET'])
def get_users():
    """
    Function to retrieve all users from the MySQL database
    :return: database users
    """
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))
