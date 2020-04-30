from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.patent import PatentClassification
import xml.etree.ElementTree as ET
import werkzeug, os

parser = reqparse.RequestParser()
parser.add_argument('Accept', type=str, required=True, location='headers')

class Process(Resource):

    def get(self, uniqueid):
        
        return {
                'data':'<classification><modelVersion>1.7.0</modelVersion><status>success</status><results><result><rank>1</rank><cpc>G01S5/00</cpc><confidence>0.07051900029182434</confidence></result><result><rank>2</rank><cpc>H04W4/00</cpc><confidence>0.0347851999104023</confidence></result><result><rank>3</rank><cpc>G08G1/00</cpc><confidence>0.00120623002294451</confidence></result></results></classification>',
                'message':'uniqueid = {}'.format(uniqueid),
                'status':'success'
                }

