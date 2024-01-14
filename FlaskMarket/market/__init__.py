from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# in __init__.py

from flask_migrate import Migrate

app = Flask(__name__)
 # Assuming 'db' is your SQLAlchemy instance

# ... other configurations and imports ...

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
# migrate = Migrate(app, db) 
app.config['SECRET_KEY'] = 'e16df18613c418c72063083a'
db = SQLAlchemy(app)
# migrate = Migrate(app, db) 
#hash password of user
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view="login_page"
login_manager.login_message_category='info'
from market import routes

