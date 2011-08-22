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
    """ Generic Exception for Etymdendron """
    pass
class EtymExceptDB(EtymException):
    """ A database-related exception """
    pass
class EtymExceptWord(EtymException):
    """ A word-related exception """
    pass

###
# Functions
def loadDB(filename):
    """ This function loads the word database given by filename 

        Right now with the XML backend, I read and parse the file.

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

        This is using the XML backend.

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
        the values the element text.

        For example, details = {'lang':'Modern English', 
            'def':'To dance lively', 
            'text': ['bigdance','coolstep','befrobingate'] }

        Remember the 'lang' and 'def' elements contain only a string, 
        whereas there can be more than one 'text' element. These text 
        elements are stored in a list.

    """
    if word == []:
        raise EtymExceptWord('No word given for loadWordDetails')

    wordDets = {'lang': None, 'def': None, 'text': None, 
                'morpheme': None, 'tag': None}
    
    wordDets['lang'] = word.xpath('lang')[0].text
    wordDets['def'] = word.xpath('def')[0].text
    wordDets['morpheme'] = word.xpath('morpheme')[0].text
    wordDets['text'] = [n.text for n in word.xpath('text')]
    wordDets['tag'] = word.tag

    return wordDets

def editWordDetails(word, details):
    """ Edits the element word using details

        details is a dict where the keys are the element names and 
        the values the element text.

        For example, details = {'lang':'Modern English', 
            'def':'To dance lively', 
            'text': ['bigdance','coolstep','befrobingate'] }

        Remember the 'lang' and 'def' elements contain only a string, 
        whereas there can be more than one 'text' element. These text 
        elements are stored in a list.

        If an entry is set to None, the element value is replaced by a 
        space (since one element of each kind (lang, def, text) must exist.

    """
    # First check sanity of the input details
    element_items = ['lang', 'text', 'morpheme', 'def']
    for item in element_items:
        if item not in details.keys():
            raise EtymExceptWord('Required key(s) not found in word details'
                    '\n details: {0}'.format(details))
    if type(details['text']) is not list:
        raise EtymExceptWord("'text' value is not a list")

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

    Output is a list, each item is a parent.
    Each item is the ElementTree node for each parent.
    If no parents are found, then it returns None.

    NB: I can't specify more than one parent in XML, 
    so this doesn't return a list.

    """
    return word.getparent()

def loadWordChildren(word):
    """ This returns the child(ren) of a given word

    Output is a list, each item is a child word.
    Each item is the ElementTree node for each child.
    If no children are found, then it returns [].

    """
    return word.xpath('word')

def countWordChildren(word):
    """ Returns how many children a word has """
    return len(word.xpath('word'))

def createWord(word_details, word_parent=None, word_children=None):
    """ Creates a new word given the word_details dictionary
    
    word_details is a dictionary in the same format as editWordDetails.
    That is, the keys are ['lang', 'text', 'def', 'morpheme'].
    All of the values are strings, except 'text' is a list of strings.

    It returns a new Element object with the right setup. It needs to be
    added to a tree by specifying parent/children. This can be done later
    or it can be done here by using word_parent, word_children.

    If word_details['tag'] = 'tree' then a new tree is created. There 
    cannot be a word_parent, and there MUST be at least one word_children.

    """
    # Make sure we have some word_details
    if word_details is None:
        raise EtymExceptWord('No word_details specified!')

    # Are we creating a word element or a tree root?
    if 'tag' in word_details:
        tag = word_details['tag']
    else:
        tag = 'word'

    # Create the new word element or tree element
    if tag == 'word':
        new_word = ET.Element(tag)
    elif tag == 'tree':
#        if word_parent is not None:
#            raise EtymExceptWord("Can't specify a parent ({0}) to "
#                                 "a tree ({1})".format(word_parent,
#                                                       word_details))
        if word_children is None:
            raise EtymExceptWord("Must specify at least one child")

        new_word = ET.Element(tag)

    # Append children words
    if word_children is not None:
        editWordChildren(new_word, word_children)

    # Add in the details
    if word_details:
        editWordDetails(new_word, word_details)
    else:
        raise EtymExceptWord('No word_details specified!')

    # Attach to parent word
    if word_parent is not None:
        editWordParent(new_word, word_parent)

    # Return the newly created word
    return new_word

def validateWord(word):
    """ Validates the elements of a word

    word is an Element object and is checked that it follows the DTD.
    If all the subelements exist (lang, def, subwords, etc), then it
    rewrites them in the proper order.

    """

    if word is None:
        raise EtymExceptWord('word is None!')

    # First check the tag
    if word.tag not in ['word', 'tree', 'etym']:
        raise EtymExceptWord('Invalid word tag (tag={0})'.format(word.tag))

    # Check all of the subelements are present in right numbers
    if word.tag in ['word', 'tree']:
        test_items = {'lang':0, 'text':0, 'morpheme':0, 'def':0, 'word':0}
        word_items = [child.tag for child in word]
        for item in word_items:
            if item not in test_items.keys():
                # Only allowable items are allowed
                raise EtymExceptWord('Extra item(s) found in word details'
                        '\n details: {0}'.format(word_items))
            else:
                test_items[item] += 1

        # Need at least one of the following
        for item in ['lang', 'text', 'morpheme', 'def']:
            if test_items[item] < 1:
                raise EtymExceptWord('Required item "{0}" not found in word details'
                    '\n details: {1}'.format(item, word_items))

        # Need at most one of the following
        for item in ['lang', 'def']:
            if test_items[item] > 1:
                raise EtymExceptWord('Too many of "{0}" found in word details'
                    '\n details: {1}'.format(item, word_items))

        # Now put the items in the right order
        word_dets = loadWordDetails(word)
        editWordDetails(word, word_dets)

    return True

def editWordChildren(word, children):
    """ Changes the children of a word

    word is some Element object and children is a list of Element object(s).
    This **OVERWRITES** the links to any extant children with those specified.

    If children is None or [] then it severs the extant children from 
    the word.

    """

    num_children = 0
    if children is not None:
        if type(children) is list:
            num_children = len(children)
        else:
            num_children = 1
            children = [children] # wrap the child in a list

    # Check that each child is valid
    if num_children > 0:
        for child in children:
            validateWord(child)

    # Remove extant children
    for child in word.iterchildren(tag='word'):
        word.remove(child)

    # Add in the new ones
    if num_children > 0:
        for child in children:
            word.append(child)

def editWordParent(word, parent):
    """ Changes the parent of a word

    word is some Element object and parent is another Element object.
    If word already has a parent, that link to the old parent is 
    overwritten with this one.

    If parent is None, then it severs the word (and its descendants)
    from the tree.

    """

    # Check inputs
    validateWord(word)
    if parent is not None:
        validateWord(parent)

    # Sever the word from its old parent
    old_parent = word.getparent()
    if old_parent is not None:
        for child in old_parent.iterchildren(tag='word'):
            if child == word:
                old_parent.remove(child)

    # Attach it to its new one
    if parent is not None:
        parent.append(word)

def deleteWord(word):
    """ Deletes the word from the tree

    If word is a part of tree (has parent/children), then it severs the link
    first by attaching any children to parent (the grandparent 
    of the children) and then modifies the word so it no longer 
    has parent or children.

    The word is then removed from the tree.

    """

    # Check input
    validateWord(word)

    # Load in parent and children
    word_children = loadWordChildren(word)
    word_parent = loadWordParents(word)

    # Attach the children to the new parent
    for child in word_children:
        editWordParent(child, word_parent)

    # Sever the word from its parent
    editWordParent(word, None)

def moveWord(source, dest):
    """ Moves a word in the tree to a different location

    source and dest are both valid words in the same tree. Children of
    source and maintained so they're present in dest.

    source is the word to be moved. This routine attaches it to be a child
    of dest.

    This is just a wrapper (possibly unneeded) for editWordParent()

    """
    validateWord(source)
    validateWord(dest)

    editWordParent(source, dest)

def findRoot(word):
    """ Returns the tree root for a given word """
    return word.xpath('ancestor::tree')[0]

def checkNode(word):
    """ Checks the word and returns the type 

    Returns 'word' or 'tree' depending on if it's a word or a tree root.
    Raises an exception if the word is invalid.

    """
    if word is None:
        raise EtymExceptWord('word is None')

    return word.tag

def deleteTree(tree):
    """ Removes the tree and all its children from the XML db """

    # Check input
    validateWord(tree)

    # Sever the tree from the db
    tree.clear()

def addTree(word_db, tree_details, children):
    """ Add a tree to the XML db 

    tree_details is a dict with keys: 'lang', 'def', 'text', 'morpheme'.
    children is a list of children to add to the tree. There **MUST** be
    at least one child to add to the tree.
    
    """
    # Some argument checking
    if children is None:
        raise EtymExceptWord("'children' is None")
    elif type(children) is not list:
        raise EtymExceptWord("'children' argument is not a list")
    elif len(children) < 1:
        raise EtymExceptWord("'children' argument is empty")

    if word_db is None:
        raise EtymExceptDB("'word_db' argument is invalid")

    # Check sanity of the details dictionary
    element_items = ['lang', 'text', 'morpheme', 'def']
    for item in element_items:
        if item not in tree_details.keys():
            raise EtymExceptWord('Required key(s) not found in word details'
                    '\n details: {0}'.format(tree_details))
    if type(tree_details['text']) is not list:
        raise EtymExceptWord("'text' value is not a list")

    tree_details['tag'] = 'tree'

    # Find the root etym element (it's the parent of each tree)
    etym_root = word_db.getroot()

    # Now we can create the tree
    createWord(tree_details, word_parent=etym_root, word_children=children)

# EOF

