import setuptools

import dweet2ser

# except ImportError:
#    from distutils.core import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dweet2ser',
    version=dweet2ser.__version__,
    author='Zach Henry',
    author_email='zhenry9@gmail.com',
    description='A dweet.io <-> serial interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zhenry9/dweet2ser',
    download_url='https://github.com/zhenry9/dweet2ser/archive/0.1.0.tar.gz',
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
        # 'dweepy',  packaging modified dweepy source with dweet2ser_conductor for now
        'requests >= 2, < 3',
        'pySerial',
        'colorama',
        'termcolor',
        # my patched dweepy repo, no longer needed
        # 'dweepy @ https://github.com/zhenry9/dweepy/archive/master.tar.gz',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dweet2ser = dweet2ser.__main__:main',
        ]
    },
    zip_safe=False,
)
