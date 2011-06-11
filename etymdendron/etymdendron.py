#!/usr/bin/env python

# This file is the main driver for the program

###
# Imports
import sys
import argparse

import cli_funcs

###
# Global constants

def main():
    """ The main routine """
    ###
    # Parse arguments
    parser = argparse.ArgumentParser(description='Run etymdendron')
    parser.add_argument('word', help='Word to search for (will be asked for if not specified)', nargs='?', default=None)
    args = parser.parse_args()

    ###
    # First let's load the XML

    ###
    # Search for a word
    if args.word is None:
        search_word = cli_funcs.get_search_word()
    else:
        search_word = args.word

    ###
    # Display the tree

    ###
    # That's all!
    sys.exit(0)

if __name__ == '__main__':
    main()
