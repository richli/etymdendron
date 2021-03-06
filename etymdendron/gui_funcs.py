#!/usr/bin/env python
""" This module contains classes and such needed for the GUI """

# We're using wxWidgets as a cross-platform toolkit
import wx
import wx.xrc
import os.path
from global_opts import WORDS_FILE
import common_funcs as cf

# Define the application
class EtymApp(wx.App):
    """ Our subclass implementation of App"""
###
# Initialization
    def OnInit(self):
        """ Load in the XRC file and display frame """
        etympath = os.path.dirname(__file__)
        etymxrc = os.path.join(etympath, 'etym.xrc')
        self.xrc = wx.xrc.XmlResource(etymxrc)
        self.InitUI()
        # Override the tight fitting of the sizers; this is also a 
        # workaround since the frame size is set before the menubar is
        # loaded, so it pushes the content down
        self.frame.SetMinSize(wx.Size(610, 395)) 
        # Initialize some other variables
        #self.search_on_select = False
        self.current_node = None
        self.edit_mode = False
        self.UpdateUi_edit()
        # Put focus in the search box
        self.searchbox.SetFocus()
        return True

    def InitUI(self):
        """ Load the frame, bind events, and show """
        self.frame = self.xrc.LoadFrame(None, 'et_Frame')
        # Bind menu events
        self.frame.Bind(wx.EVT_MENU, self.OnQuit, id=wx.xrc.XRCID('m_exit'))
        self.frame.Bind(wx.EVT_MENU, self.OnAbout, id=wx.xrc.XRCID('m_about'))
        self.frame.Bind(wx.EVT_MENU, self.OnLoad, id=wx.xrc.XRCID('m_load'))
        self.frame.Bind(wx.EVT_MENU, self.OnSave, id=wx.xrc.XRCID('m_save'))
        self.frame.Bind(wx.EVT_MENU, self.OnNewTree,
                        id=wx.xrc.XRCID('m_newtree'))
        # Bind button events
        self.frame.Bind(wx.EVT_BUTTON, self.OnSearch,
                id=wx.xrc.XRCID('et_btnSearch'))
        self.frame.Bind(wx.EVT_TEXT_ENTER, self.OnSearch,
                id=wx.xrc.XRCID('et_boxSearch'))
        self.frame.Bind(wx.EVT_CHOICE, self.OnMorphemeSelect,
                id=wx.xrc.XRCID('et_choice'))
        self.frame.Bind(wx.EVT_CHECKBOX, self.OnEdit,
                id=wx.xrc.XRCID('et_checkEdit'))
        self.frame.Bind(wx.EVT_BUTTON, self.OnEditSave,
                id=wx.xrc.XRCID('et_btnEditSave'))
        self.frame.Bind(wx.EVT_BUTTON, self.OnEditRevert,
                id=wx.xrc.XRCID('et_btnEditRevert'))
        # Bind text events
#        self.frame.Bind(wx.EVT_TEXT, self.OnDetailEdit,
#                id=wx.xrc.XRCID('et_txtLang'))
#        self.frame.Bind(wx.EVT_TEXT, self.OnDetailEdit,
#                id=wx.xrc.XRCID('et_txtDef'))
#        self.frame.Bind(wx.EVT_TEXT, self.OnDetailEdit,
#                id=wx.xrc.XRCID('et_txtAlt'))
        #self.frame.Bind(wx.EVT_CHECKBOX, self.OnSearchCheck,
        #       id=wx.xrc.XRCID('et_checkSearch'))
        # Bind tree events
        self.frame.Bind(wx.EVT_TREE_SEL_CHANGED, self.SelectTreeItem,
                id=wx.xrc.XRCID('et_tree'))
        self.frame.Bind(wx.EVT_TREE_ITEM_MENU, self.MenuTreeItem,
                id=wx.xrc.XRCID('et_tree'))
        self.frame.Bind(wx.EVT_TREE_BEGIN_DRAG, self.DragTreeItem,
                id=wx.xrc.XRCID('et_tree'))
        self.frame.Bind(wx.EVT_TREE_END_DRAG, self.DropTreeItem,
                id=wx.xrc.XRCID('et_tree'))
        # Save some object references for later
        self.searchbox = wx.xrc.XRCCTRL(self.frame, 'et_boxSearch')
        self.treebox = wx.xrc.XRCCTRL(self.frame, 'et_tree')
        self.langbox = wx.xrc.XRCCTRL(self.frame, 'et_txtLang')
        self.defbox = wx.xrc.XRCCTRL(self.frame, 'et_txtDef')
        self.altbox = wx.xrc.XRCCTRL(self.frame, 'et_txtAlt')
        self.searchchoice = wx.xrc.XRCCTRL(self.frame, 'et_choice')
        self.searchbtn = wx.xrc.XRCCTRL(self.frame, 'et_btnSearch')
        self.editchk = wx.xrc.XRCCTRL(self.frame, 'et_checkEdit')
        self.editbtn_save = wx.xrc.XRCCTRL(self.frame, 'et_btnEditSave')
        self.editbtn_revert = wx.xrc.XRCCTRL(self.frame, 'et_btnEditRevert')
        self.menubar = self.frame.GetMenuBar()
        self.menu_newtree = self.menubar.FindItemById(wx.xrc.XRCID('m_newtree'))
        
        # And show the frame!
        self.frame.Show()

###
# Event handlers
    def OnAbout(self, event):
        """ Displays the About dialog """
        dlg = wx.MessageDialog(self.frame,
                'Etymdendron \nAn etymology tree viewer\n'
                'Written 2011 Rich Li','About Etymdendron', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnQuit(self, event):
        """ Exits the program """
        self.frame.Close(True)

    def OnLoad(self, event):
        """ Loads the word database """
        dlg = wx.FileDialog(self.frame, 'Choose the database file',
                defaultFile = WORDS_FILE, wildcard = '*.xml',
                style = wx.OPEN | wx.FILE_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.LoadWordDB(dlg.GetPath())
        dlg.Destroy()

    def OnSave(self, event):
        """ Saves the word database """
        dlg = wx.FileDialog(self.frame, 'Choose the database file',
                defaultFile = WORDS_FILE, wildcard = '*.xml',
                style = wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.SaveWordDB(dlg.GetPath())
        dlg.Destroy()

    def OnSearch(self, event):
        """ Searches for a word, displays results """
        self.search_word = self.searchbox.GetValue()
        if self.search_word is not '': # Simple validation for now
            num_trees, matched_words = cf.searchDB(self.words_tree,
                    self.search_word)
            self.treebox.DeleteAllItems() # Clear the tree control out
            self.searchchoice.Clear() # Clear out the choice box
            self.searchchoice.Disable()
            wx.xrc.XRCCTRL(self.frame, 'et_txtLang').SetEditable(self.edit_mode)
            wx.xrc.XRCCTRL(self.frame, 'et_txtDef').SetEditable(self.edit_mode)
            wx.xrc.XRCCTRL(self.frame, 'et_txtAlt').SetEditable(self.edit_mode)
            if num_trees == 0:
                chosen_root = chosen_word = None
            elif num_trees > 1:
                # Populate the tree with the first match
                chosen_root = matched_words[0][0]
                chosen_word = [match[1] for match in matched_words]
                # Populate the choice button
                for item in matched_words:
                    word = item[1]
                    word_details = cf.loadWordDetails(word)
                    choice_text = '{0} ({1})'.format(
                            word_details['morpheme'], word_details['lang'])
                    self.searchchoice.Append(choice_text, item)

                self.searchchoice.Enable()
                self.searchchoice.SetSelection(0)
            else:
                # Extract the tree and all matched words separately
                # Just pick the first entry (m_w[...][0] are the 
                # same in this case)
                chosen_root = matched_words[0][0]
                chosen_word = [match[1] for match in matched_words]

            self.search_root = chosen_root
            self.search_words = chosen_word
            self.DisplayTree(self.search_root, self.search_words)

    def OnMorphemeSelect(self, event):
        """ Chooses between different morphemes (different trees) """
        item = event.GetClientData()
        self.treebox.DeleteAllItems()
        self.DisplayTree(item[0], item[1])

#    def OnSearchCheck(self, event):
#        """ Toggles whether we search on selected word or not """
#        self.search_on_select = not self.search_on_select
#        self.searchbox.Enable(not self.searchbox.IsEnabled())
#        self.searchbtn.Enable(not self.searchbtn.IsEnabled())

    def OnEdit(self, event):
        """ Just saves whether we're in edit mode or not """
        self.edit_mode = event.IsChecked()
        self.UpdateUi_edit()

    def UpdateUi_edit(self):
        """ Update UI elements depending on edit mode """
        if self.current_node is None:
            self.editchk.Disable()
        else:
            self.editchk.Enable()
        self.langbox.SetEditable(self.edit_mode)
        self.defbox.SetEditable(self.edit_mode)
        self.altbox.SetEditable(self.edit_mode)
        self.editbtn_save.Enable(self.edit_mode)
        self.editbtn_revert.Enable(self.edit_mode)
        self.menu_newtree.Enable(self.edit_mode)

    def OnEditSave(self, event):
        """ Save word details """
        # Create new details dictionary
        new_nodeDetails = {}
        new_nodeDetails['lang'] = self.langbox.GetValue()
        new_nodeDetails['def'] = self.defbox.GetValue()
        alt_list = [text_item.strip() for text_item in
                self.altbox.GetValue().split(',')]
        new_nodeDetails['text'] = alt_list 
        # Set the morpheme to be the first text entry
        new_nodeDetails['morpheme'] = alt_list[0]

        # Save the word details
        cf.editWordDetails(self.current_node, new_nodeDetails)
        # Refresh the tree
        self.DisplayTree(self.search_root, self.search_words)

    def OnEditRevert(self, event):
        """ Revert word details """
        self.UpdateWordDetails()

    def OnNewTree(self, event):
        """ Create a new tree """
        # Create a tree with some default values
        tree_dets = {'text': ['NEW ROOT'], 'morpheme': 'NEW ROOT', 'lang':
                     'UNKNOWN', 'def': 'Change me!', 'tag': 'tree'}
        word_dets = {'text': ['NEW WORD'], 'morpheme': 'NEW WORD', 'lang':
                     'UNKNOWN', 'def': 'Change me!'}
        new_word = cf.createWord(word_dets)
        new_tree = cf.addTree(self.words_tree, tree_dets, [new_word])
        # Refresh the tree
        self.search_root = new_tree
        self.search_words = None
        self.DisplayTree(self.search_root, self.search_words)

###
# Some methods for the class
    def LoadWordDB(self, filename=WORDS_FILE):
        """ Load the database file """
        self.words_tree = cf.loadDB(filename)
        if type(self.words_tree) is str:
            dlg_err = wx.MessageDialog(self.frame, self.words_tree
                ,'Error', wx.OK|wx.ICON_EXCLAMATION)
            dlg_err.ShowModal()
            dlg_err.Destroy()
            self.words_tree = None
        else:
            print('{0} loaded, {1} trees found'.format(filename,
            len(self.words_tree.getroot())))

    def SaveWordDB(self, filename=WORDS_FILE):
        """ Saves the database file """
        cf.saveDB(self.words_tree, filename)
        print('{0} saved with {1} trees'.format(filename,
            len(self.words_tree.getroot())))

    def DisplayTree(self, root, nodes, select=None):
        """ Displays the tree in the wx.TreeCtrl object 

            root is the ElementTree root node.
            nodes is a list of ElementTree word nodes to emphasize.
            If root is None, then is displays an empty tree message.
            select is a word that is selected (focused), this overrides
            focusing on any emphasized nodes.
        """
        self.treebox.DeleteAllItems()
        if root is None:
            self.treebox.AddRoot('No matches found')
            self.editchk.Disable()
            self.editchk.SetValue(False)
            self.editbtn_save.Disable()
            self.editbtn_revert.Disable()
            self.langbox.ChangeValue('')
            self.defbox.ChangeValue('')
            self.altbox.ChangeValue('')
            self.selected_node = None
        else:
            root_details = cf.loadWordDetails(root)
            root_elem = self.treebox.AddRoot(root_details['text'][0],
                    data = wx.TreeItemData(root))
            if type(nodes) is not list:
                nodes = [nodes]
            self._populate_tree(root, root_elem, nodes, select)
            self.treebox.ExpandAll()
            self.editchk.Enable()

    def _populate_tree(self, node, node_elem, emph_nodes, select):
        """ Recursive private function to fill in the rest of the tree control 

            node: the ElementTree element we're working on.
            node_elem: the corresponding object in the TreeCtrl class.
            emph_nodes: a list of ElementTree elements, 
            these will be emphasized.
            select: an element that will be selected (focused). If not None
            then it overrides focusing on emphasized nodes.

        """
        # len() of a node returns how many children it has
        if cf.countWordChildren(node) > 0:
            for child in cf.loadWordChildren(node):
                child_details = cf.loadWordDetails(child)
                # Just display the first alternate
                child_label = child_details['text'][0] 
                child_elem = self.treebox.AppendItem(node_elem, child_label,
                        data = wx.TreeItemData(child))
                if child in emph_nodes and select is None:
                    # Emphasize the node
                    self.treebox.SetItemBold(child_elem)
                    # Select the node
                    self.treebox.SelectItem(child_elem)
                if select is not None and child == select:
                    self.treebox.SelectItem(child_elem)
                # Recurse!
                self._populate_tree(child, child_elem, emph_nodes, select)

    def DragTreeItem(self, event):
        """ Initiate a drag-and-drop for the tree """
        # This is only allowable under edit mode
        if self.edit_mode:
            self._drag_node = self.treebox.GetPyData(event.GetItem())
            node_type = cf.checkNode(self._drag_node)
            # We let words be moved, but not the tree root
            if node_type == 'word':
                event.Allow()
            elif node_type == 'tree':
                event.Veto()

    def DropTreeItem(self, event):
        """ Finish a drop-and-drop for the tree """
        self._drop_node = self.treebox.GetPyData(event.GetItem())
        # Can't drop onto a child of the self._drag_node (infinite loop)
        if cf.isDescendant(self._drag_node, self._drop_node):
            event.Veto()
        else:
            # Okay, move the word
            cf.moveWord(self._drag_node, self._drop_node)
            # Refresh the tree
            self.DisplayTree(self.search_root, self.search_words,
                             select=self._drop_node)

    def MenuTreeItem(self, event):
        """ Right-click menu for a tree item """
        self.current_node = self.treebox.GetPyData(event.GetItem())
        # Create the menu
        menu = wx.Menu()
        www_item_id = wx.NewId()
        menu.Append(www_item_id, 'Lookup on etymonline')
        menu.AppendSeparator()
        child_item_id = wx.NewId()
        menu.Append(child_item_id, 'Add child word')
        sib_item_id = wx.NewId()
        menu.Append(sib_item_id, 'Add sibling word')
        del_item_id = wx.NewId()
        menu.Append(del_item_id, 'Delete word')
        # Disable items if not in edit mode
        if not self.edit_mode:
            menu.Enable(child_item_id, False)
            menu.Enable(sib_item_id, False)
            menu.Enable(del_item_id, False)
        # Disable add sibling if we're on the root word (no parent)
        if cf.loadWordDetails(self.current_node)['tag'] == 'tree':
            menu.Enable(sib_item_id, False)
        # Bind events
        menu.Bind(wx.EVT_MENU, self.TreeItemLookupWWW, id=www_item_id)
        menu.Bind(wx.EVT_MENU, self.TreeItemAddChild, id=child_item_id)
        menu.Bind(wx.EVT_MENU, self.TreeItemAddSib, id=sib_item_id)
        menu.Bind(wx.EVT_MENU, self.TreeItemDelete, id=del_item_id)
        # Show the menu
        self.treebox.PopupMenu(menu)

    def TreeItemLookupWWW(self, event):
        """ Lookup an entry on etymonline """
        lookup_word = cf.loadWordDetails(self.current_node)
        wx.LaunchDefaultBrowser('http://www.etymonline.com/index.php?' 
                                'term={0}'.format(lookup_word['morpheme']))

    def TreeItemDelete(self, event):
        """ Delete the selected tree item """
        # Find what type of node it is (word or tree root)
        node_type = cf.checkNode(self.current_node)
        # Delete the word or tree
        if node_type == 'word':
            cf.deleteWord(self.current_node)
        elif node_type == 'tree':
            cf.deleteTree(self.current_node)
            self.search_root = self.search_words = None
        # Refresh the tree
        self.DisplayTree(self.search_root, self.search_words)

    def TreeItemAddChild(self, event):
        """ Add a child to the selected tree item """
        # Create a word with some default values
        #wordDets = cf.loadWordDetails(self.current_node)
        word_dets = {'text': ['NEW WORD'], 'morpheme': 'NEW WORD', 'lang':
                     'UNKNOWN', 'def': 'Change me!'}
        new_word = cf.createWord(word_dets, word_parent=self.current_node)
        # Refresh the tree
        self.DisplayTree(self.search_root, self.search_words, select=new_word)

    def TreeItemAddSib(self, event):
        """ Add a sibling to the selected tree item """
        # Create a word with some default values
        #wordDets = cf.loadWordDetails(self.current_node)
        word_dets = {'text': ['NEW WORD'], 'morpheme': 'NEW WORD', 'lang':
                     'UNKNOWN', 'def': 'Change me!'}
        new_word = cf.createWord(word_dets,
                      word_parent=cf.loadWordParents(self.current_node))
        # Refresh the tree, select new word
        self.DisplayTree(self.search_root, self.search_words, select=new_word)

    def SelectTreeItem(self, event):
        """ Find what tree item has been selected and then update UI """
        self.current_node = self.treebox.GetPyData(event.GetItem())
        self.UpdateWordDetails()

    def UpdateWordDetails(self):
        """ Update various widgets when a tree item has been selected """
        # Set the 'word details' widgets
        nodeDetails = cf.loadWordDetails(self.current_node)
        alt_text = ', '.join(nodeDetails['text'])
        self.langbox.ChangeValue(nodeDetails['lang'])
        self.defbox.ChangeValue(nodeDetails['def'])
        self.altbox.ChangeValue(alt_text)

#        # Update the search word if applicable
#        if self.search_on_select:
#            self.search_word = node.xpath('text')[0].text
#            self.searchbox.SetValue(self.search_word)
#            # TODO: bold, debold the tree control

        # Highlight matching alternates, if applicable
        if self.search_word in alt_text:
            # Set the style
            bold_style = self.altbox.GetDefaultStyle()
            bold_font = bold_style.GetFont()
            bold_font.SetWeight(wx.FONTWEIGHT_BOLD)
            bold_style.SetFont(bold_font)
            # Find the start/end indices
            str_start = alt_text.find(self.search_word)
            # Bold the word
            self.altbox.SetStyle(str_start,
                    str_start+len(self.search_word),bold_style)

###
# Validators?

#class SearchValidator(wx.PyValidator):
#    def Validate(self, window):
#        pass

