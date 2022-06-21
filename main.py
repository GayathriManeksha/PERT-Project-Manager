from app import app
from app import db


if __name__ == '__main__':  
   y=db.create_all() 
   app.run(debug = True)  