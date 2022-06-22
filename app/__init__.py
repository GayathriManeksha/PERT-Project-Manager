from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nodes.sqlite3'  
app.config['SECRET_KEY'] = "secret key"  
  
db = SQLAlchemy(app)  
from app import routes
from app.database import User

login_manager = LoginManager()
login_manager.login_view = 'signin'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
