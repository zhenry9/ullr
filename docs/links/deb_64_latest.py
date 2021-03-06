import requests

from . import link
from . import vers

latest_release_info = requests.get('https://api.github.com/repos/zhenry9/ullr/releases/latest').json()
url = 'https://github.com/zhenry9/ullr/releases/latest'
for asset in latest_release_info['assets']:
    if asset['browser_download_url'].endswith('amd64.deb'):
        url = asset['browser_download_url']

link_name = "deb_64_latest"
user_text = "Latest Debian(amd64) Release"

link.xref_links.update({link_name: (user_text, url)})