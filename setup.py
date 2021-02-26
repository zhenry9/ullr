import setuptools

from dweet2ser import __version__ as version

# except ImportError:
#    from distutils.core import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dweet2ser',
    version=version,
    author='Zach Henry',
    author_email='zhenry9@gmail.com',
    description='A dweet.io <-> serial interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zhenry9/dweet2ser',
    download_url=f'https://github.com/zhenry9/dweet2ser/archive/{version}.tar.gz',
    packages=setuptools.find_packages(exclude=('tests',)),
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
    ],
    install_requires=[
        "colorama>=0.4.4, <1",
        "Flask>=1.1.2, <2",
        "Flask-SocketIO>=5.0.1, <6",
        "pyserial>=3.5, <4",
        "requests>=2.25.1, <3",
        "termcolor>=1.1.0, <2"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dweet2ser = dweet2ser.__main__:main',
        ]
    },
    zip_safe=False,
)
