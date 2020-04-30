from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.patent import PatentModel
import xml.etree.ElementTree as ET
import werkzeug, os
from werkzeug.utils import secure_filename
import uuid
from call_ext import send_patent_ext, get_patent_precla_ext
import sqlite3
from flask import Flask, Response
from call_int import get_pred_int
from models.classification import ClassificationModel
import time


uniqueid = str(uuid.uuid4())

parser = reqparse.RequestParser()
parser.add_argument('data',type=werkzeug.datastructures.FileStorage, location='files')
parser.add_argument('Accept', type=str, required=True, location='headers')
parser.add_argument('Content-MD5', type=str, required=True, location='headers')   

url = 'http://127.0.0.1:5000/patent/classification/'

class Patent(Resource):
 
    decorators=[]

    def post(self):
        data = parser.parse_args()
        Content_Ash_Key = data['Content-MD5']
       
        if data['data'] == "":
            return {
                    'data':'',
                    'message':'No file found',
                    'status':'error'
                    }
        
        zipfile = data['data'].read()
        
        filename = secure_filename(data['data'].filename)


        if zipfile:
            Link = send_patent_ext(zipfile, Content_Ash_Key)
            patent = PatentModel(uniqueid=uniqueid, patentid=filename[:-4], filename=filename, zipfile=zipfile, extuuid=Link[-36:], req_time = time.time())
            patent.save_to_db()
            response = get_pred_int(zipfile, filename)
            n = 1
            for item in response:
                rank = n
                precla_symbol = item[0]
                confidence = item[1]
                preclassification = ClassificationModel( uniqueid=uniqueid , patentid = filename[:-4]  , rank = rank, precla_symbol = precla_symbol, confidence =  confidence, source = 'Internal', class_time = time.time() )
                preclassification.save_to_db()
                n += 1 
            return Response(headers={'Link': url + uniqueid, 'Original-Link': Link})
        
        return {
                'data':'',
                'message':'Something when wrong',
                'status':'error'
                }
