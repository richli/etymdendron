#!/usr/bin/env python
""" This module holds functions common to both GUI and CLI clients """

###
# Imports
import sys
try:
    from lxml import etree as ET
except ImportError as err:
    print('lxml is missing\n{0}'.format(err))

###
# Functions
def loadDB(filename):
    """ This function loads the word database given by filename 
        Right now with the XML backend, I read and parse the file
    """
    words_db = ET.ElementTree()
    try:
        words_db.parse(filename,ET.XMLParser(dtd_validation=True))
    except ET.XMLSyntaxError as err:
        err_msg = "ERROR: Error parsing {0}\n{1}".format(filename,err)
        return err_msg
    except IOError as err:
        err_msg = "ERROR: Error reading {0}\n{1}".format(filename,err)
        return err_msg

    return words_db
