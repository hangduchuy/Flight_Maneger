from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_babelex import Babel
import cloudinary


app = Flask(__name__)
app.secret_key = '$#&*&%$(*&^(*^*&%^%$#^%&^%*&56547648764%$#^%$&^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/saleapp?charset=utf8mb4' % quote('246938')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['CART_KEY'] = 'cart'

db = SQLAlchemy(app=app)
login = LoginManager(app=app)
babel = Babel(app=app)

cloudinary.config(
  cloud_name = "dcwl3jhhm",
  api_key = "646768638842992",
  api_secret = "q5LACc5cxYG8hgJymqgT02xOS64"
)


@babel.localeselector
def load_locale():
    return 'vi'
