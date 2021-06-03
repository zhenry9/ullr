from . import link
from . import vers

link_name = "source"
user_text = "Ullr Source (tarball)"
url = f'https://github.com/zhenry9/ullr/archive/{vers}.tar.gz'

link.xref_links.update({link_name: (user_text, url)})