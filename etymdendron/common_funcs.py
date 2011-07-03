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
class EtymExceptWord(EtymException):
    pass

###
# Functions
def loadDB(filename):
    """ This function loads the word database given by filename 
        Right now with the XML backend, I read and parse the file
    """
    words_db = ET.ElementTree()
    try:
        words_db.parse(filename, ET.XMLParser(dtd_validation=True,
            remove_blank_text=True))
    except ET.XMLSyntaxError as err:
        raise EtymExceptDB("ERROR: Error parsing {0}\n{1}".format(
            filename, err))
    except IOError as err:
        raise EtymExceptDB("ERROR: Error reading {0}\n{1}".format(
            filename, err))

    return words_db

def saveDB(words_db, filename):
    """ This saves words_db into filename
        This is using the XML backend
    """
    with open(filename, 'w') as f:
        f.write(ET.tostring(words_db, encoding='utf-8', pretty_print=True,
            xml_declaration=True, standalone=True))

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
    if word is None:
        raise EtymExceptWord('No word given for loadWordDetails')

    wordDets = {'lang': None, 'def': None, 'text': None, 'morpheme': None}
    
    wordDets['lang'] = word.xpath('lang')[0].text
    wordDets['def'] = word.xpath('def')[0].text
    wordDets['morpheme'] = word.xpath('morpheme')[0].text
    wordDets['text'] = [n.text for n in word.xpath('text')]

    return wordDets

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
    # First check sanity of the word
    element_items = ['lang', 'text', 'morpheme', 'def']
    for item in element_items:
        if item not in details.keys():
            raise EtymExceptWord('Required key(s) not found in word details'
                    '\n details: {0}'.format(details))

    # Create the new Element objects
    new_elements = []
    for item in element_items:
        if item == 'text': # details[item] is a list in this case
            for text_items in xrange(len(details[item])):
                new_element = ET.Element(item)
                new_element.text = details[item][text_items]
                new_elements.append(new_element)
        else:
            new_element = ET.Element(item)
            new_element.text = details[item]
        new_elements.append(new_element)

    # Save subword(s) and remove them from tree
    for child in word.iterchildren(tag='word'):
        new_elements.append(child)
        word.remove(child)

    # Clear out the old elements
    for item in element_items:
        for child in word.iterchildren(tag=item):
            word.remove(child)

    # Add the new ones, including the saved subwords
    for item in new_elements:
        word.append(item)

def loadWordParents(word):
    """ This returns the parent(s) of a given word
    Output is a tuple, each item is a parent
    Each item is the ElementTree node for each parent
    If no parents are found, then it returns (None,)

    """
    raise NotImplementedError

def loadWordChildren(word):
    """ This returns the child(ren) of a given word
    Output is a tuple, each item is a child word
    Each item is the ElementTree node for each child
    If no children are found, then it returns (None,)

    """
    raise NotImplementedError
