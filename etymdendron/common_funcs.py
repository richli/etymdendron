#!/usr/bin/env python
""" This module holds functions common to both GUI and CLI clients """

###
# Imports
try:
    from lxml import etree as ET
except ImportError as im_err:
    print('lxml is missing\n{0}'.format(im_err))

###
# Exceptions
class EtymException(Exception):
    pass
class EtymExceptDB(EtymException):
    pass

###
# Functions
def loadDB(filename):
    """ This function loads the word database given by filename 
        Right now with the XML backend, I read and parse the file
    """
    words_db = ET.ElementTree()
    try:
        words_db.parse(filename, ET.XMLParser(dtd_validation=True))
    except ET.XMLSyntaxError as err:
        raise EtymExceptDB("ERROR: Error parsing {0}\n{1}".format(
            filename, err))
    except IOError as err:
        raise EtymExceptDB("ERROR: Error reading {0}\n{1}".format(
            filename, err))

    return words_db

def searchDB(word_db, search_word):
    """ Searches the database word_db for the word search_word
        Returns a tuple: (num_trees, words)
        The 'words' element is itself a list of tuples: 
            [(tree,word), (tree,word), ...]
    """
     # We go through each of the possible trees
    matched_words = []
    found_roots = set()
    num_trees = 0
    for tree in word_db.getroot().iterchildren():
        for word in tree.iterdescendants(tag='word'):
            for text in word.iterchildren(tag='text'):
                if text.text == search_word:
                    # Alright, we found a match
                    # Add the root to our list
                    if tree not in found_roots:
                        num_trees += 1
                    found_roots.add(tree)
                    # Add the found word to our list
                    matched_words.append((tree, word))

    return (num_trees, matched_words)

def loadWordDetails(word):
    """ Returns the details of the element word
        details is a dict where the keys are the element names and 
        the values the element text

        For example, details = {'lang':'Modern English', 
            'def':'To dance lively', 
            'text': ['bigdance','coolstep','befrobingate'] }
        Remember the 'lang' and 'def' elements contain only a string, 
        whereas there can be more than one 'text' element. These text 
        elements are stored in a list.
    """
    raise NotImplementedError

def editWordDetails(word, details):
    """ Edits the element word using details
        details is a dict where the keys are the element names and 
        the values the element text

        For example, details = {'lang':'Modern English', 
            'def':'To dance lively', 
            'text': ['bigdance','coolstep','befrobingate'] }
        Remember the 'lang' and 'def' elements contain only a string, 
        whereas there can be more than one 'text' element. These text 
        elements are stored in a list.

        If an entry is set to None, the element value is replaced by a 
        space (since one element of each kind (lang, def, text) must exist.

    """
    raise NotImplementedError
