from setuptools import setup

APP = ['DjangoApp.py']
MODULES = ['os','sys','psutil','webbrowser','shlex','subprocess','signal','decimal','Cookie','cgi',
    'htmlentitydefs','smtplib','BaseHTTPServer', 'imghdr','sndhdr','wx','sqlite3','docutils',
    'compiler']
	
PACKAGES = ['django','email','logging']
DATA_FILES = ['icons','MyProject']

OPTIONS = {'includes':MODULES, 'packages': PACKAGES}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
