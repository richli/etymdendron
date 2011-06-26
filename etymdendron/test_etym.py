#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
""" Testing framework for etymdendron 
    Uses the unittest framework in the stdlib
"""

import unittest
import sys
from lxml import etree as ET
import global_opts
import common_funcs as cf
import cli_funcs as cli
import StringIO

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

    def testReadWord(self):
        """ Test reading the details of a word """
        db = cf.loadDB(global_opts.WORDS_FILE)
        num_trees, matched_words = cf.searchDB(db, 'horse')
        #chosen_root = matched_words[0][0]
        chosen_word = matched_words[0][1]
        wordDets = cf.loadWordDetails(chosen_word)
        self.assertEqual(wordDets['lang'],'Middle English')
        self.assertEqual(wordDets['def'],'A horse that you feed oats')
        self.assertEqual(wordDets['text'],['horse','hors','horce','horsse','horis','hos','ors'])

    @unittest.skip('Not yet implemented')
    def testEditWord(self):
        """ Test editing a word details """
        db = cf.loadDB(global_opts.WORDS_FILE)
        #TODO: search for some word; save its details; write new details; compare new details with old details

    @unittest.skip('Not yet implemented')
    def testAddWord(self):
        """ Test adding a word """
        raise NotImplementedError

    @unittest.skip('Not yet implemented')
    def testDelWord(self):
        """ Test deleting a word """
        raise NotImplementedError

    @unittest.skip('Not yet implemented')
    def testAddTree(self):
        """ Test adding a tree """
        raise NotImplementedError

    @unittest.skip('Not yet implemented')
    def testDelTree(self):
        """ Test deleting a tree """
        raise NotImplementedError

class EtymDisplayCLI(unittest.TestCase):
    dispHorse = u'''Root: khursa (PIE)
  Child: hors (Old English, "A man-eating beast")
    Child: *horse*, hors, horce, horsse, horis, hos, ors (Middle English, "A horse that you feed oats")
      Child: *horse* (Modern English, "A horse that you ride")
  Child: hors (Old Frisian, "A horse")
  Child: ros, hros (Old High German, "Eine Bestie")
    Child: ros (Middle High German, "Eines infizierten Tieres")
      Child: ross (Modern High German, "Eine blutrünstige Monster")
  Child: hross (Old Norse, "A horse")'''

    dispRos = u'''Root: khursa (PIE)
  Child: hors (Old English, "A man-eating beast")
    Child: horse, hors, horce, horsse, horis, hos, ors (Middle English, "A horse that you feed oats")
      Child: horse (Modern English, "A horse that you ride")
  Child: hors (Old Frisian, "A horse")
  Child: *ros*, hros (Old High German, "Eine Bestie")
    Child: *ros* (Middle High German, "Eines infizierten Tieres")
      Child: ross (Modern High German, "Eine blutrünstige Monster")
  Child: hross (Old Norse, "A horse")'''

    def setUp(self):
        self.db = cf.loadDB(global_opts.WORDS_FILE)

    def testSearchHorse(self):
        """ Tests how many trees 'horse' is found in """
        num_trees, matched_words = cf.searchDB(self.db, 'horse')
        self.assertEqual(num_trees, 1)

    def testDispHorse(self):
        """ Tests the CLI display of 'horse' """
        num_trees, matched_words = cf.searchDB(self.db, 'horse')
        chosen_root = matched_words[0][0]
        chosen_word = [match[1] for match in matched_words]
        # Redirect stdout to a string
        tree_output = StringIO.StringIO()
        sys.stdout = tree_output
        cli.display_tree(chosen_root, chosen_word, 'horse')
        tree_output_string = tree_output.getvalue()
        sys.stdout = sys.__stdout__
        self.maxDiff = None
        self.assertEqual(tree_output_string.strip(), self.dispHorse)

    def testDispRos(self):
        """ Tests the CLI display of 'ros' """
        num_trees, matched_words = cf.searchDB(self.db, 'ros')
        chosen_root = matched_words[0][0]
        chosen_word = [match[1] for match in matched_words]
        # Redirect stdout to a string
        tree_output = StringIO.StringIO()
        sys.stdout = tree_output
        cli.display_tree(chosen_root, chosen_word, 'ros')
        tree_output_string = tree_output.getvalue()
        sys.stdout = sys.__stdout__
        self.maxDiff = None
        self.assertEqual(tree_output_string.strip(), self.dispRos)

    def testSearchBiology(self):
        """ Tests how many trees 'biology' is found in """
        num_trees, matched_words = cf.searchDB(self.db, 'biology')
        self.assertEqual(num_trees, 2)

    def testSearchNonexistant(self):
        """ Tests how many trees an unknown word is found in """
        num_trees, matched_words = cf.searchDB(self.db, 'kumquat')
        self.assertEqual(num_trees, 0)
    
if __name__ == '__main__':
    unittest.main()
