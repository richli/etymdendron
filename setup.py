#!/usr/bin/env python

from distutils.core import setup
#import py2exe # not on linux; save this for later

setup(  name='etymdendron',
        version='0.50',
        packages=['etymdendron'],
        package_dir={'etymdendron': 'etymdendron'},
        package_data={'etymdendron': ['words.xml','etym.xrc','etym-gui.pyw']},
        data_files=['TODO'],
        description=['Etymology tree viewer'],
        author='Rich Lindsley',
        author_email='richli.ff@gmail.com',
        url='http://github.com/richli/etymdendron')

# Notes to myself:
# To create the source distribution in dist/, run ./setup.py sdist
