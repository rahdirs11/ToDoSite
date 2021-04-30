from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
# from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
# loginManager = LoginManager(app)

from todo import routes
