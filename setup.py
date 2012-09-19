from setuptools import setup, find_packages

import staticwraps

setup(
    name='django-staticwraps',
    maintainer='Cox Media Group Digital & Strategy Open Source Team',
    maintainer_email='opensource@coxinc.com',
    url='http://github.com/coxmediagroup',
    version=staticwraps.__version__,
    description='reads static content from the filesystem to be wrapped in our sites',
    packages=find_packages(),
    install_requires=[
        'django-jsonfield==0.8.10',
        'BeautifulSoup==3.0.8.1',
    ],
)
