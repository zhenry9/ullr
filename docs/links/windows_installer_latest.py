import requests

from . import link
from . import vers

# it seems that this request will not point to the correct release on a new tagged commit
latest_release_info = requests.get('https://api.github.com/repos/zhenry9/ullr/releases/latest').json()
url = 'https://github.com/zhenry9/ullr/releases/latest'
for asset in latest_release_info['assets']:
    if asset['browser_download_url'].endswith('.msi'):
        url = asset['browser_download_url']

link_name = "windows_latest"
user_text = "Latest Windows Release"

link.xref_links.update({link_name: (user_text, url)})