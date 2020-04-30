import requests
from flask import Flask
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from flask_restful import Resource, reqparse, Api
import werkzeug, os
from werkzeug.utils import secure_filename
import sqlite3
import io
import chardet
from lxml import objectify
import json


app = Flask(__name__)
api = Api(app)

AV_SERVER="http://145.64.2.81/preclassification/patent"

proxies = {
    'http': 'http://proxylb.internal.epo.org:8080/',
    'https': 'http://gsbloxy02.internal.epo.org:8080',
}

session = requests.Session()
session.proxies = proxies 

def requests_retry_session(
    retries=3,
    backoff_factor=0.5,
    status_forcelist=(500, 502, 504,503, 407),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_patent_precla_ext(extuuid):
    url = AV_SERVER + '/classification/' + extuuid
    print(url)
 
    result = requests.request("GET", url, proxies = proxies, timeout = 10)
    
    return objectify(json.dumps(result.text))      

class Classification(Resource):
    def get(self, uniqueid):
        #extuuid = PatentClassification.find_by_uniqueid(uniqueid).extuuid
        #print (uniqueid + ' ' + extuuid)
        print(uniqueid)
        precla = get_patent_precla_ext(uniqueid)
        print(precla)
        return precla
 
api.add_resource(Classification,'/patent/classification/<string:uniqueid>')

if __name__ == '__main__':
    app.run(debug=True)