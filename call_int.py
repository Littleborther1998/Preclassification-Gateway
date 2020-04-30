import pip._vendor.requests as requests
from pip._vendor.requests.adapters import HTTPAdapter
from pip._vendor.requests.packages.urllib3.util.retry import Retry
import os
import codecs
from werkzeug.utils import secure_filename


INT_SERVER="https://nautilus.internal.epo.org/ds-precla-test/classify-file"


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

def get_pred_int(f, g):
    headers = {'Accept': 'application/xml'}
    filename = g
    files = {'zipfile': (filename, f, 'application/zip')}
    r = requests_retry_session(session=requests.Session()).post(INT_SERVER, files = files, verify=False)
    r = r.json()
    return list(zip(r['classes'], [round(k,4) for k in r['scores']]))
    

 
