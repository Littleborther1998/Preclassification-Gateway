from flask import Flask
from flask_restful import  Api
#from flask_jwt import JWT
#import sqlite3
from db import db
from resources.patent import Patent
#from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Mat'
api =  Api(app)

#jwt = JWT(app, authenticate, identity)

api.add_resource(Patent, '/patent')
#api.add_resource(Patent, '/patent/classification/<string:uniqueId>')


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)