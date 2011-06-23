#!/usr/bin/env python
""" Testing framework for etymdendron 
    Uses the unittest framework in the stdlib
"""

import unittest
from lxml import etree as ET
import global_opts
import common_funcs as cf

class EtymDB(unittest.TestCase):
    """ Various tests for the database """
    def testTypeDB(self):
        """ Test if the return type is what we expect """
        db = cf.loadDB(global_opts.WORDS_FILE)
        self.assertIsInstance(db, type(ET.ElementTree()))

    def testLoadBadDB(self):
        """ Test if it correctly throws an exception for a file not found """
        self.assertRaises(cf.EtymExceptDB, cf.loadDB, 'sdf')

    @unittest.skip('Not yet implemented')
    def testSaveDB(self):
        """ Test saving the db """
        raise NotImplementedError

    @unittest.skip('Not yet devised the test')
    def testSearchWord(self):
        raise NotImplementedError
    
if __name__ == '__main__':
    unittest.main()
