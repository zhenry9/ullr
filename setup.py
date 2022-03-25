try:
    import setuptools

except ImportError:
    from distutils.core import setup
    from io import open

from ullr import __version__ as version

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Ullr',
    version=version,
    author='Zach Henry',
    author_email='zhenry9@gmail.com',
    description='A serial <-> MQTT interface for sports timing.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://ullr.rtfd.io',
    # download_url=f'https://github.com/zhenry9/ullr/archive/{version}.tar.gz',
    packages=setuptools.find_packages(exclude=('tests',)),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
    ],
    install_requires=[
        "astroid~=2.8.5",
        "bidict~=0.21.4",
        "certifi~=2021.10.8",
        "chardet~=4.0.0",
        "charset-normalizer~=2.0.7",
        "click~=8.0.3",
        "colorama~=0.4.4",
        "dnspython~=2.1.0",
        "docopt~=0.6.2",
        "Flask~=2.0.2",
        "Flask-SocketIO~=5.1.1",
        "idna~=3.3",
        "importlib-metadata~=4.8.2",
        "isort~=5.10.1",
        "itsdangerous~=2.0.1",
        "Jinja2~=3.0.3",
        "lazy-object-proxy~=1.6.0",
        "MarkupSafe~=2.0.1",
        "mccabe~=0.6.1",
        "ntplib~=0.4.0",
        "paho-mqtt~=1.6.1",
        "platformdirs~=2.4.0",
        "psutil~=5.8.0",
        "pylint~=2.11.1",
        "pyserial~=3.5",
        "python-engineio~=4.3.0",
        "python-socketio~=5.5.0",
        "requests~=2.26.0",
        "six~=1.16.0",
        "termcolor~=1.1.0",
        "toml~=0.10.2",
        "typed-ast~=1.5.0",
        "typing-extensions~=4.0.0",
        "urllib3~=1.26.7",
        "Werkzeug~=2.0.2",
        "wrapt~=1.13.3",
        "yarg~=0.1.9",
        "zipp~=3.6.0",
        "zope.event~=4.5.0",
        "zope.interface~=5.4.0"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ullr = ullr.__main__:main',
        ]
    },
    zip_safe=False,
)
