from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import xml.etree.ElementTree as ET
from call_ext import get_patent_precla_ext
from flask import Flask, Response
import json
from models.classification import ClassificationModel
from models.patent import PatentModel
import time

class Classification(Resource):
    def get(self, uniqueid):
        patent_req = PatentModel.find_by_uniqueid(uniqueid)
        extuuid = patent_req.extuuid
        patentid  = patent_req.patentid
        precla_averbis = get_patent_precla_ext(extuuid)
        precla_internal_list = ClassificationModel.find_by_uniqueid(uniqueid)
        precla_int_results = list()
        precla_int_result = dict()
        for item in precla_internal_list:
            precla_int_results.append({'rank': item.rank, 'precla_symbol': item.precla_symbol, 'confidence' : item.confidence} )
        print(precla_int_results)    
        root = precla_averbis.getroot()
        precla_averbis_results = list()
        precla_averbis_result = dict()
        
        for elem in root.findall("./results/result"):
            for child in elem:
                precla_averbis_result[child.tag]  = child.text
            precla_averbis_results.append(precla_averbis_result)
            preclassification = ClassificationModel( uniqueid=uniqueid , patentid = patentid  , rank = precla_averbis_result['rank'], precla_symbol = precla_averbis_result['cpc'], confidence =  precla_averbis_result['confidence'], source = 'Averbis', class_time = time.time())          
            preclassification.save_to_db()
            precla_averbis_result = dict()

        return Response(json.dumps(precla_averbis_results), status=200, mimetype='application/json')

      
      