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



app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('data',type=werkzeug.datastructures.FileStorage, location='files')
url = "https://nautilus.internal.epo.org/ds-precla-test/classify-file"
INF_SERVER="https://nautilus.internal.epo.org/ds-precla-test/classify-file"


session = requests.Session()


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

class Patent(Resource):

    def post(self):
            data = parser.parse_args()
            zipfile = data['data']
        
            filename = secure_filename(data['data'].filename)
            files = {
              'zipfile': (filename, zipfile.read(), 'application/zip')
              #'zipfile': open('D:\PreCla\EP16150002.zip', 'rb')
            }

            response = requests_retry_session(session=requests.Session()).post(url, files = files , verify = False)
            #response = requests_retry_session(session=requests.Session()).post(INF_SERVER, files={'zipfile': zipfile}, verify=False)
            print(response.json())

api.add_resource(Patent,'/patent')

if __name__ == '__main__':
    app.run(debug=True)