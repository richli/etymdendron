#!/usr/bin/env python

from distutils.core import setup
import os
import shutil
#import py2exe # not on linux; save this for later

# Create the documentation
os.chdir('doc')
os.system('make html')
os.chdir('..')
# Move the doc
shutil.copytree('doc/_build/html', 'documentation')

# Create the distribution
setup(  name='etymdendron',
        version='0.50',
        packages=['etymdendron'],
        package_dir={'etymdendron': 'etymdendron'},
        package_data={'etymdendron': ['words.xml', 'etym.xrc']},
        data_files=[('.', ['TODO', 'run.pyw'])],
        description=['Etymology tree viewer'],
        author='Rich Lindsley',
        author_email='richli.ff@gmail.com',
        url='http://github.com/richli/etymdendron')

shutil.rmtree('documentation')

# Notes to myself:
# To create the source distribution in dist/, run ./setup.py sdist
