#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
""" Testing framework for etymdendron 

    Uses the unittest framework in the stdlib.
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

    def testCountWordChildren(self):
        """ Tests counting word children """
        # This word shouldn't have any children
        chosen_word = self.getWord('hross')
        word_children = cf.countWordChildren(chosen_word)
        self.assertEqual(word_children, 0)
        # This word should have one child
        chosen_word = self.getWord('far')
        word_children = cf.countWordChildren(chosen_word)
        self.assertEqual(word_children, 1)
        # This word should have two children
        chosen_word = self.getWord('porcus')
        word_children = cf.countWordChildren(chosen_word)
        self.assertEqual(word_children, 2)

    def testEditWordDetails(self):
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

    def testCreateWord(self):
        """ Test creating a new word """
        # Try some bad inputs
        word_dets = None
        self.assertRaises(cf.EtymExceptWord, cf.createWord, word_dets)
        word_dets = {}
        self.assertRaises(cf.EtymExceptWord, cf.createWord, word_dets)
        word_dets = {'lang': 'English'}
        self.assertRaises(cf.EtymExceptWord, cf.createWord, word_dets)
        word_dets = {'lang': 'English', 'text': 'banana',
                'morpheme': 'bannana', 'def': 'A fruity thing'}
        self.assertRaises(cf.EtymExceptWord, cf.createWord, word_dets)

        # Now a good input, test the output
        word_dets = {'lang': 'English', 'text': ['banana', 'pineapple'],
                'morpheme': 'bannana', 'def': 'A fruity thing',
                     'tag': 'word'}
        new_word = cf.createWord(word_dets)
        new_word_details = cf.loadWordDetails(new_word)
        self.assertEqual(word_dets, new_word_details)

        # Try creating a word with a specified parent/children
        child_dets = {'lang': 'Spanglish', 'text': ['strawberry'],
                'morpheme': 'strawberry', 'def': 'A fruity thing'}
        parent_dets = {'lang': 'Fromesian', 'text': ['raspberry'],
                'morpheme': 'raspberry', 'def': 'A fruity thing'}
        word_dets = {'lang': 'English', 'text': ['banana'],
                'morpheme': 'banana', 'def': 'A fruity thing'}
        new_child = cf.createWord(child_dets)
        new_parent = cf.createWord(parent_dets)
        new_word = cf.createWord(word_dets, word_parent=new_parent,
                                 word_children = new_child)
        self.assertEqual(cf.loadWordChildren(new_word)[0], new_child)
        self.assertEqual(cf.loadWordParents(new_word), new_parent)

    def testValidateWord(self):
        """ Tests validating a word """
        # Test a known good word
        chosen_word = self.getWord('far')
        self.assertEqual(cf.validateWord(chosen_word), True)

        # Test some bad words
        # wrong tag
        test_word = ET.Element('gook')
        self.assertRaises(cf.EtymExceptWord, cf.validateWord, test_word)
        # right tag, no text
        test_word = ET.Element('word')
        self.assertRaises(cf.EtymExceptWord, cf.validateWord, test_word)
        # good tag and text, no details
        test_word.text = 'testing'
        self.assertRaises(cf.EtymExceptWord, cf.validateWord, test_word)
        # Create some incomplete details
        word_det = ET.Element('lang')
        word_det.text = 'asdf'
        test_word.append(word_det)
        self.assertRaises(cf.EtymExceptWord, cf.validateWord, test_word)
        word_det = ET.Element('def')
        word_det.text = 'lkjfs'
        test_word.append(word_det)
        self.assertRaises(cf.EtymExceptWord, cf.validateWord, test_word)
        word_det = ET.Element('morpheme')
        word_det.text = 'sdf0'
        test_word.append(word_det)
        self.assertRaises(cf.EtymExceptWord, cf.validateWord, test_word)
        word_det = ET.Element('text')
        word_det.text = '23rds'
        test_word.append(word_det)
        word_det = ET.Element('text')
        word_det.text = '230oudsf'
        test_word.append(word_det)
        self.assertEqual(cf.validateWord(chosen_word), True)
        # Make sure it gets saved in the right order
        test_word = ET.Element('word')
        word_det = ET.Element('text')
        word_det.text = '23rds'
        test_word.append(word_det)
        test_word.text = 'testing'
        word_det = ET.Element('def')
        word_det.text = 'lkjfs'
        test_word.append(word_det)
        word_det = ET.Element('text')
        word_det.text = '203fjklsdfj'
        test_word.append(word_det)
        word_det = ET.Element('lang')
        word_det.text = 'asdf'
        test_word.append(word_det)
        word_det = ET.Element('morpheme')
        word_det.text = 'sdf0'
        test_word.append(word_det)
        cf.validateWord(test_word)
        sort_output = ('<word>testing<lang>asdf</lang><text>23rds</text>'
        '<text>203fjklsdfj</text><morpheme>sdf0</morpheme>'
        '<def>lkjfs</def></word>')
        self.assertEqual(ET.tostring(test_word), sort_output)

    def testChangeChildren(self):
        """ Tests modifying the children of a word """
        chosen_word = self.getWord('far')
        real_children = cf.loadWordChildren(chosen_word)
        word_dets = {'lang': 'English', 'text': ['banana', 'pineapple'],
                'morpheme': 'bannana', 'def': 'A fruity thing'}
        test_child = cf.createWord(word_dets)
        cf.validateWord(test_child)

        # Test output with good input
        # (chosen_word only has one child)
        new_children = list(real_children)
        new_children.append(test_child)
        cf.editWordChildren(chosen_word, new_children)
        self.assertEqual(cf.countWordChildren(chosen_word), 2)

        # This removes children from chosen_word
        cf.editWordChildren(chosen_word, None)
        self.assertEqual(cf.countWordChildren(chosen_word), 0)
        self.assertEqual(cf.loadWordParents(real_children[0]), None)
        self.assertEqual(cf.loadWordParents(test_child), None)

        # Let's add a child back on
        cf.editWordChildren(chosen_word, test_child)
        self.assertEqual(cf.countWordChildren(chosen_word), 1)
        self.assertEqual(cf.loadWordParents(test_child), chosen_word)

    def testChangeParent(self):
        """ Tests modifying the parent of a word """
        # This word has a parent, 'equinus'
        chosen_word = self.getWord('equine')
        # Make sure it can read the parent
        test_parent = cf.loadWordParents(chosen_word)
        parent_details = cf.loadWordDetails(test_parent)
        self.assertEqual(parent_details['text'], ['equinus'])
        self.assertEqual(parent_details['lang'], 'Latin')
        # Add a new word and set its parent
        word_dets = {'lang': 'English', 'text': ['banana', 'pineapple'],
                'morpheme': 'bannana', 'def': 'A fruity thing'}
        new_word = cf.createWord(word_dets)
        cf.editWordParent(new_word, test_parent)
        self.assertEqual(cf.countWordChildren(test_parent), 2)
        self.assertEqual(cf.countWordChildren(chosen_word), 0)
        cf.editWordParent(new_word, chosen_word)
        self.assertEqual(cf.countWordChildren(chosen_word), 1)
        # Add a new word and it to be parent to a word
        new_word = cf.createWord(word_dets)
        cf.editWordParent(chosen_word, new_word)
        self.assertEqual(new_word, cf.loadWordParents(chosen_word))

    def testDelWord(self):
        """ Test deleting a word """
        # This parent I've chosen has only one child
        db = self.getDB()
        num_trees, matched_words = cf.searchDB(db, 'varch')
        test_parent = matched_words[0][1]
        num_trees, matched_words = cf.searchDB(db, 'ferkel')
        test_word = matched_words[0][1]

#        # Test deleting a word that's not in the tree?
#        word_dets = {'lang': 'English', 'text': ['banana', 'pineapple'],
#                'morpheme': 'bannana', 'def': 'A fruity thing'}
#        orphan_word = cf.createWord(word_dets)
#        self.assertRaises(cf.EtymExceptWord, cf.deleteWord, orphan_word)

        # Test deleting a word
        cf.deleteWord(test_word)
        self.assertEqual(cf.loadWordChildren(test_parent), [])
        num_trees, matched_words = cf.searchDB(db, 'ferkel')
        self.assertEqual(num_trees, 0)

        # Reload the db, delete the parent and ensure the child moves up
        db = self.getDB()
        num_trees, matched_words = cf.searchDB(db, 'varch')
        test_parent = matched_words[0][1]
        num_trees, matched_words = cf.searchDB(db, 'ferkel')
        test_word = matched_words[0][1]
        test_grandparent = cf.loadWordParents(test_parent)
        cf.deleteWord(test_parent)
        self.assertEqual(cf.loadWordParents(test_word), test_grandparent)

    def testMoveWord(self):
        """ Test moving a word to a different location in the tree """
        db = self.getDB()
        # Here we move ross to be a child of hross
        # First get references to the words
        num_trees, matched_words = cf.searchDB(db, 'ross')
        test_source = matched_words[0][1]
        test_source_parent = cf.loadWordParents(test_source)
        num_trees, matched_words = cf.searchDB(db, 'hross')
        test_dest_parent = matched_words[0][1]
        self.assertEqual(cf.countWordChildren(test_dest_parent), 0)
        # Perform the move
        cf.moveWord(test_source, test_dest_parent)
        # Make sure it really happened
        self.assertEqual(cf.countWordChildren(test_dest_parent), 1)
        self.assertEqual(cf.countWordChildren(test_source_parent), 0)
        self.assertEqual(cf.loadWordParents(test_source), test_dest_parent)

        # Let's test for some bad inputs
        self.assertRaises(cf.EtymExceptWord, cf.moveWord, None, None)
        self.assertRaises(cf.EtymExceptWord, cf.moveWord, test_source, None)
        self.assertRaises(cf.EtymExceptWord, cf.moveWord, None, test_source)

        # Another test, this time make sure the children are maintained
        # We move fearh (which has a child and a grandchild) to be a child
        # of porcus (which has two children and a few further descendants)
        db = self.getDB()
        # First get references to the words
        num_trees, matched_words = cf.searchDB(db, 'fearh')
        test_source = matched_words[0][1]
        test_source_parent = cf.loadWordParents(test_source)
        num_trees, matched_words = cf.searchDB(db, 'porcus')
        test_dest_parent = matched_words[0][1]
        self.assertEqual(cf.countWordChildren(test_dest_parent), 2)
        self.assertEqual(cf.countWordChildren(test_source), 1)
        # Perform the move
        cf.moveWord(test_source, test_dest_parent)
        # Make sure it really happened
        self.assertEqual(cf.countWordChildren(test_dest_parent), 3)
        self.assertEqual(cf.countWordChildren(test_source_parent), 2)
        self.assertEqual(cf.loadWordParents(test_source), test_dest_parent)
        self.assertEqual(cf.countWordChildren(test_source), 1)
        num_trees, matched_words = cf.searchDB(db, 'far')
        test_dest_child = matched_words[0][1]
        self.assertEqual(cf.loadWordParents(test_dest_child), test_source)

    def testFindRoot(self):
        """ Test finding the tree root of a word """
        # Search for biology, since it's in two trees
        db = self.getDB()
        # First get references to the words
        num_trees, matched_words = cf.searchDB(db, 'biology')
        test_source = matched_words[0][1]
        test_root = matched_words[0][0]
        self.assertEqual(num_trees, 2)
        # Find the root
        tree_root = cf.findRoot(test_source)
        tree_root_details = cf.loadWordDetails(tree_root)
        # Confirm it's right
        self.assertEqual(tree_root_details['lang'], 'PIE')
        self.assertEqual(tree_root_details['morpheme'], 'gweie')
        self.assertEqual(test_root, tree_root)
        # Now try the other biology tree
        test_source = matched_words[1][1]
        test_root = matched_words[1][0]
        # Find the root
        tree_root = cf.findRoot(test_source)
        tree_root_details = cf.loadWordDetails(tree_root)
        # Confirm it's right
        self.assertEqual(tree_root_details['lang'], 'PIE')
        self.assertEqual(tree_root_details['morpheme'], 'leg')
        self.assertEqual(test_root, tree_root)

    def testIsDescendant(self):
        """ Test checking IsDescendant() """
        # "farho" is a great grand-parent of "farrow"
        # "porcus" is a sibling of "farho"
        db = self.getDB()
        num_trees, matched_words = cf.searchDB(db, 'farho')
        test_top = matched_words[0][1]
        num_trees, matched_words = cf.searchDB(db, 'farrow')
        test_bottom = matched_words[0][1]
        num_trees, matched_words = cf.searchDB(db, 'porcus')
        test_side = matched_words[0][1]

        self.assertEqual(cf.isDescendant(test_top, test_bottom), True)
        self.assertEqual(cf.isDescendant(test_top, test_side), False)
        self.assertEqual(cf.isDescendant(test_bottom, test_top), False)
        self.assertEqual(cf.isDescendant(test_bottom, test_side), False)


    def testCheckNode(self):
        """ Test checking the node type """
        db = self.getDB()
        num_trees, matched_words = cf.searchDB(db, 'fearh')
        test_source = matched_words[0][1]
        test_root = matched_words[0][0]
        self.assertEqual(cf.checkNode(test_source), 'word')
        self.assertRaises(cf.EtymExceptWord, cf.checkNode, None)
        self.assertEqual(cf.checkNode(test_root), 'tree')

    def testDelTree(self):
        """ Test deleting a tree """
        # Search for biology, since it's in two trees
        db = self.getDB()
        # First get references to the words
        num_trees, matched_words = cf.searchDB(db, 'biology')
        test_source = matched_words[0][1]
        self.assertEqual(num_trees, 2)
        tree_root = cf.findRoot(test_source)
        # Delete a tree
        cf.deleteTree(tree_root)
        # Confirm it happened
        num_trees, matched_words = cf.searchDB(db, 'biology')
        test_source = matched_words[0][1]
        self.assertEqual(num_trees, 1)
        tree_root = cf.findRoot(test_source)
        # Try again
        cf.deleteTree(tree_root)
        # Confirm it happened (again)
        num_trees, matched_words = cf.searchDB(db, 'biology')
        self.assertEqual(num_trees, 0)

    def testAddTree(self):
        """ Test adding a tree """
        # Create a test word to attach to the new tree
        word_dets = {'lang': 'English', 'text': ['banana', 'pineapple'],
                'morpheme': 'banana', 'def': 'A fruity thing',
                     'tag': 'word'}
        new_word = cf.createWord(word_dets)
        new_word_details = cf.loadWordDetails(new_word)
        self.assertEqual(word_dets, new_word_details)
        # Create the new tree
        db = self.getDB()
        tree_dets = {'lang': 'PIE', 'text': ['bane'],
                'morpheme': 'bane', 'def': 'Some fruit',
                     'tag': 'tree'}
        cf.addTree(db, tree_dets, [new_word])
        # Test that it was created
        num_trees, matched_words = cf.searchDB(db, 'banana')
        search_word = matched_words[0][1]
        search_root = matched_words[0][0]
        search_root_dets = cf.loadWordDetails(search_root)
        self.assertEqual(search_word, new_word)
        self.assertEqual(search_root_dets['lang'], 'PIE')
        self.assertEqual(search_root_dets['def'], 'Some fruit')
        self.assertEqual(search_root_dets['morpheme'], 'bane')
        self.assertEqual(search_root_dets['text'], ['bane'])

        # Okay, now test some bad input
        # second arg not a list
        self.assertRaises(cf.EtymExceptWord, cf.addTree, 
                          db, tree_dets, new_word)
        # No word given
        self.assertRaises(cf.EtymExceptWord, cf.addTree, 
                          db, tree_dets, [None])
        self.assertRaises(cf.EtymExceptWord, cf.addTree, 
                          db, tree_dets, [])
        # Invalid db
        self.assertRaises(cf.EtymExceptDB, cf.addTree, 
                          None, tree_dets, [new_word])
        # Bad tree details
        tree_dets = {'lang': 'PIE', 'text': 'bane',
                'morpheme': 'bane', 'tag': 'tree'}
        self.assertRaises(cf.EtymExceptWord, cf.addTree, 
                          db, tree_dets, [new_word])

class EtymDisplayCLI(unittest.TestCase):
    """ Various tests for the CLI display """
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
