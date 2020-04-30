import pip._vendor.requests as requests
from pip._vendor.requests.adapters import HTTPAdapter
from pip._vendor.requests.packages.urllib3.util.retry import Retry
import json
from xml.etree.ElementTree import fromstring, ElementTree



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

def send_patent_ext(zipfile, MD5):  
    headers = {'Accept': 'text/xml','Content-MD5': MD5}
    files = [
              ('data', zipfile)
            ]  
    try:
        r2 = requests_retry_session(session=requests.Session()).post(AV_SERVER, proxies = proxies, headers = headers ,files = files, verify = False)   
        r2 = r2.headers['Link']
        return(r2)

    except:
        return{'message':'not finding'}

def get_patent_precla_ext(extuuid):
    url = AV_SERVER + '/classification/' + extuuid
    result = requests.request("GET", url, proxies = proxies, timeout = 10)
    tree = ElementTree(fromstring(result.text))
    return tree