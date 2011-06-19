#!/usr/bin/env python
""" This module contains classes and such needed for the GUI """

# We're using wxWidgets as a cross-platform toolkit
import os
import wx
import wx.xrc
from global_opts import WORDS_FILE
from common_funcs import loadDB, searchDB

# Define the application
class EtymApp(wx.App):
    """ Our subclass implementation of App"""
###
# Initialization
    def OnInit(self):
        """ Load in the XRC file and display frame """
        self.xrc = wx.xrc.XmlResource('etym.xrc')
        self.InitUI()
        #self.Show(True)
        return True

    def InitUI(self):
        """ Load the frame, bind events, and show """
        self.frame = self.xrc.LoadFrame(None, 'et_Frame')
        # Bind menu events
        self.frame.Bind(wx.EVT_MENU, self.OnQuit, id=wx.xrc.XRCID('m_exit'))
        self.frame.Bind(wx.EVT_MENU, self.OnAbout, id=wx.xrc.XRCID('m_about'))
        self.frame.Bind(wx.EVT_MENU, self.OnLoad, id=wx.xrc.XRCID('m_load'))
        self.frame.Bind(wx.EVT_MENU, self.OnSave, id=wx.xrc.XRCID('m_save'))
        # Bind button events
        self.frame.Bind(wx.EVT_BUTTON, self.OnSearch, id=wx.xrc.XRCID('et_btnSearch'))
        self.frame.Bind(wx.EVT_TEXT_ENTER, self.OnSearch, id=wx.xrc.XRCID('et_boxSearch'))
        # Save some object references for later
        self.searchbox = wx.xrc.XRCCTRL(self.frame,'et_boxSearch')
        self.treebox = wx.xrc.XRCCTRL(self.frame,'et_tree')
        # And show the frame!
        self.frame.Show()
        # Override the tight fitting of the sizers; this is also a 
        # workaround since the frame size is set before the menubar is
        # loaded, so it pushes the content down
        self.frame.SetMinSize(wx.Size(642,400)) 
        # Put focus in the search box
        self.searchbox.SetFocus()

###
# Event handlers
    def OnAbout(self, event):
        """ Displays the About dialog """
        dlg = wx.MessageDialog(self.frame, 'Etymdendron \nAn etymology tree viewer\n'
            'Written 2011 Rich Li','About Etymdendron', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnQuit(self, event):
        """ Exits the program """
        #import pdb; pdb.set_trace()
        self.frame.Close(True)

    def OnLoad(self, event):
        """ Loads the word database """
#TODO: Implement me
        self.dirname = ''
        dlg = wx.FileDialog(self.frame, 'Choose the database file', self.dirname, WORDS_FILE, '*.xml', wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.LoadWordDB(dlg.GetPath())
        dlg.Destroy()

    def OnSave(self, event):
#TODO: Implement me
        """ Saves the word database """
        dlg = wx.MessageDialog(self.frame, 'This function not yet implemented'
            ,'Error', wx.OK|wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnSearch(self, event):
        search_word = self.searchbox.GetValue()
        if search_word is not '': # Simple validation for now
            num_trees, matched_words = searchDB(self.words_tree, search_word)
            self.treebox.DeleteAllItems() # Clear the tree control out
            if num_trees == 0:
                chosen_root = chosen_word = None
            elif num_trees > 1:
                print('{0} is found in {1} trees'.format(search_word,num_trees))
                chosen_root = chosen_word = None
                #TODO: Implement this
                #chosen_root, chosen_word = cli_funcs.choose_word_from_many(matched_words)
            else:
                # Extract the tree and all matched words separately
                # Just pick the first entry (m_w[...][0] are the same in this case)
                chosen_root = matched_words[0][0]
                chosen_word = [match[1] for match in matched_words]

            self.DisplayTree(chosen_root, chosen_word, search_word)

###
# Some methods for the class
    def LoadWordDB(self, filename=WORDS_FILE):
        """ Load the database file """
        self.words_tree = loadDB(filename)
        if type(self.words_tree) is str:
            dlg_err = wx.MessageDialog(self.frame, self.words_tree
                ,'Error', wx.OK|wx.ICON_EXCLAMATION)
            dlg_err.ShowModal()
            dlg_err.Destroy()
            self.words_tree = None
        else:
            print('{0} loaded, {1} trees found'.format(WORDS_FILE,
            len(self.words_tree.getroot())))

    def DisplayTree(self, root, nodes, search_word):
        """ Displays the tree in the wx.TreeCtrl object 
            root is the ElementTree root node
            nodes is a list of ElementTree word nodes
            search_word is the searched-for word
            if root is None, then is displays an empty tree message
        """
        if root is None:
            self.treebox.AddRoot('No matches found')
        else:
            root_elem = self.treebox.AddRoot(root.xpath('text')[0].text,
                    data = wx.TreeItemData(root))
            if type(nodes) is not list:
                nodes = [nodes]
            self._populate_tree(root, root_elem, nodes, search_word)
            self.treebox.ExpandAll()

    def _populate_tree(self, node, node_elem, emph_nodes, search_word):
        """ Recursive private function to fill in the rest of the tree control 
            node: the ElementTree element we're working on
            node_elem: the corresponding object in the TreeCtrl class
            emph_nodes: a list of ElementTree elements, these will be emphasized
            search_word: the search_word, which is emphasized within elem_nodes
        """
        # len() of a node returns how many children it has
        if len(node.xpath('word')) > 0:
            for child in node.xpath('word'):
                texts = child.xpath('text')
                child_label = texts[0].text # Just display the first alternate
                child_elem = self.treebox.AppendItem(node_elem,child_label,
                        data = wx.TreeItemData(child))
                if child in emph_nodes:
                    # Emphasize the node
                    self.treebox.SetItemBold(child_elem)
                    # Select the node
                    self.treebox.SelectItem(child_elem)
                # Recurse!
                self._populate_tree(child, child_elem, emph_nodes, search_word)


###
# Validators?

#class SearchValidator(wx.PyValidator):
#    def Validate(self, window):
#        pass

