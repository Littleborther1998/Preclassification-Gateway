from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug, os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from resources.patent import Patent
from resources.classification import Classification
from db import db



app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PreCla.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'Mat'



api.add_resource(Classification, '/patent/classification/<string:uniqueid>')
api.add_resource(Patent,'/patent')

if __name__ == '__main__':
    db.init_app(app)
    db.create_all()
    app.run(debug=True)