#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
""" Testing framework for etymdendron 
    Uses the unittest framework in the stdlib
"""

import unittest
import sys, os
from lxml import etree as ET
import global_opts
import common_funcs as cf
import cli_funcs as cli
import StringIO

class EtymDB(unittest.TestCase):
    """ Various tests for the database """
    def testTypeDB(self):
        """ Test if the return type is what we expect """
        db = self.getDB()
        self.assertIsInstance(db, type(ET.ElementTree()))

    def testLoadBadDB(self):
        """ Test if it correctly throws an exception for a file not found """
        self.assertRaises(cf.EtymExceptDB, cf.loadDB, 'sdf')

    def testSaveDB(self):
        """ Test saving the db """
        db = self.getDB()
        tmp_file = 'tmp.xml'
        cf.saveDB(db, tmp_file)
        os.remove(tmp_file)


    def getDB(self):
        """ Helper function to load the DB """
        return cf.loadDB(global_opts.WORDS_FILE)

    def getWord(self, search_word):
        """ Helper function to load in a word """
        db = self.getDB()
        num_trees, matched_words = cf.searchDB(db, search_word)
        # Return the first match
        #chosen_root = matched_words[0][0]
        chosen_word = matched_words[0][1]
        return chosen_word

    def testReadWordDetails(self):
        """ Test reading the details of a word """
        chosen_word = self.getWord('horse')
        wordDets = cf.loadWordDetails(chosen_word)
        self.assertEqual(wordDets['lang'],'Middle English')
        self.assertEqual(wordDets['def'],'A horse that you feed oats')
        self.assertEqual(wordDets['text'],
                ['horse','hors','horce','horsse','horis','hos','ors'])

    def testReadWordParents(self):
        """ Test reading the parents of a word """
        # The root shouldn't have any parents
#TODO: Re-enable this once I can search for roots
#        chosen_word = self.getWord('khursa')
#        word_parents = cf.loadWordParents(chosen_word)
#        self.assertEqual(word_parents, None)
#        self.assertRaises(cf.EtymExceptWord, cf.loadWordDetails, word_parents[0])
        # This word should have one parent
        chosen_word = self.getWord('horse')
        word_parents = cf.loadWordParents(chosen_word)
        wordDets = cf.loadWordDetails(word_parents)
        self.assertEqual(wordDets['text'][0], 'hors')
        self.assertEqual(wordDets['lang'], 'Old English')
        self.assertEqual(wordDets['def'], 'A man-eating beast')

    def testReadWordChildren(self):
        """ Test reading the children of a word """
        # This word shouldn't have any children
        chosen_word = self.getWord('hross')
        word_children = cf.loadWordChildren(chosen_word)
        self.assertEqual(word_children, [])
        self.assertRaises(cf.EtymExceptWord, cf.loadWordDetails, word_children)
        # This word should have one child
        chosen_word = self.getWord('far')
        word_children = cf.loadWordChildren(chosen_word)
        wordDets = cf.loadWordDetails(word_children[0])
        self.assertEqual(wordDets['text'][0], 'farrow')
        self.assertEqual(wordDets['lang'], 'Modern English')
        self.assertEqual(wordDets['def'], 'An obsolete word for a pig')

    def testEditWord(self):
        """ Test editing a word details """
        chosen_word = self.getWord('horse')
        orig_wordDets = cf.loadWordDetails(chosen_word)
        new_wordDets = orig_wordDets.copy()
        new_wordDets['lang'] = 'Elvish'
        new_wordDets['def'] = 'A helpful friend'
        new_wordDets['text'] = ['horsey','neigh']
        new_wordDets['morpheme'] = 'horsey'

        # Try purposefully giving incorrect details
        test_wordDets = {}
        self.assertRaises(cf.EtymExceptWord, cf.editWordDetails,
                chosen_word, test_wordDets)

        # Try refreshing the word
        cf.editWordDetails(chosen_word, orig_wordDets)
        test_wordDets = cf.loadWordDetails(chosen_word)
        self.assertEqual(orig_wordDets, test_wordDets)

        # Try new details
        cf.editWordDetails(chosen_word, new_wordDets)
        test_wordDets = cf.loadWordDetails(chosen_word)
        self.assertEqual(new_wordDets, test_wordDets)
        self.assertNotEqual(orig_wordDets, test_wordDets)

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
