import setuptools

from ullr import __version__ as version

# except ImportError:
#    from distutils.core import setup

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
    download_url=f'https://github.com/zhenry9/ullr/archive/{version}.tar.gz',
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
        "colorama>=0.4.4, <1",
        "Flask>=1.1.2, <2",
        "Flask-SocketIO>=5.0.1, <6",
        "pyserial>=3.5, <4",
        "requests>=2.25.1, <3",
        "termcolor>=1.1.0, <2",
        "psutil>=5.8.0, <6",
        "paho-mqtt",
        "ntplib"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ullr = ullr.__main__:main',
        ]
    },
    zip_safe=False,
)
