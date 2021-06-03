from . import link
from . import vers

link_name = "windows"
user_text = "Latest Windows Release"
url = f"https://github.com/zhenry9/ullr/raw/main/windows/Ullr-{vers}.msi"

link.xref_links.update({link_name: (user_text, url)})