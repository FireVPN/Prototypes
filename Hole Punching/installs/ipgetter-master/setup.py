from distutils.core import setup
            
setup(
    name='ipgetter',
    version='0.6',
    author='Fernando Giannasi <phoemur@gmail.com>',
    url='https://github.com/phoemur/ipgetter',
    download_url = 'https://github.com/phoemur/ipgetter/tarball/0.6',

    description="Utility to fetch your external IP address",
    license="WTFPL",
    classifiers=[
        'Environment :: Console',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
    ],

    py_modules=['ipgetter'],

    long_description='''This module is designed to fetch your external IP address from the internet. It is used mostly when behind a NAT. It picks your IP 
randomly from a serverlist to minimize request overhead on a single server

If you want to add or remove your server from the list contact me on github''',
)
