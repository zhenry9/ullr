import requests
from . import __version__ as current_version

def _is_greater(x: str, y: str):
    x = x.replace('v','').split('.')
    y = y.replace('v','').split('.')
    return (x[0]>y[0] or (x[0]==y[0] and x[1]>y[1]) or (x[0]==y[0] and x[1]==y[1] and x[2]>y[2]))
    
def _get_newest_version_number_from_pypi():
    resp = requests.get('https://pypi.org/pypi/ullr/json')
    return resp.json()['info']['version']

def _get_newest_version_number_from_github():
    resp = requests.get('https://api.github.com/repos/zhenry9/ullr/releases/latest')
    return resp.json()['tag_name']

def update_available():
    try:
        return _is_greater(_get_newest_version_number_from_github(), current_version)
    except:
        return False