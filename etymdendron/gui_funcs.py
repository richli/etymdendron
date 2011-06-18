#!/usr/bin/env python
""" This module contains classes and such needed for the GUI """

# We're using wxWidgets as a cross-platform toolkit
import os
import wx
import wx.xrc
from global_opts import WORDS_FILE

# Define the main frame
class EtymApp(wx.App):
    """ Our subclass implementation of App"""

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
        self.frame.Bind(wx.EVT_MENU, self.OnExit, id=wx.xrc.XRCID('m_exit'))
        self.frame.Bind(wx.EVT_MENU, self.OnAbout, id=wx.xrc.XRCID('m_about'))
        self.frame.Bind(wx.EVT_MENU, self.OnLoad, id=wx.xrc.XRCID('m_load'))
        self.frame.Bind(wx.EVT_MENU, self.OnSave, id=wx.xrc.XRCID('m_save'))
        # And show the frame!
        self.frame.Show()
        pass



#    def InitUI(self):
#        #self.CreateStatusBar()
#
#        # Create the menus
#        fileMenu = wx.Menu()
#        helpMenu = wx.Menu()
#        menuLoad = fileMenu.Append(wx.ID_ANY,'&Load', 'Load the database file')
#        menuSave = fileMenu.Append(wx.ID_ANY,'&Save', 'Save the database file')
#        fileMenu.AppendSeparator()
#        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "End the program")
#        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About", "Information about the program")
#
#        menuBar = wx.MenuBar()
#        menuBar.Append(fileMenu,"&File")
#        menuBar.Append(helpMenu,"&Help")
#        self.SetMenuBar(menuBar)
#
#        # Define menu bindings
#        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
#        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
#        self.Bind(wx.EVT_MENU, self.OnLoad, menuLoad)
#        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
#
#        # Add a sizer and widgets
#        hbox = wx.BoxSizer(wx.HORIZONTAL)
#        vbox = wx.BoxSizer(wx.VERTICAL)
#        self.treeDisp = wx.TreeCtrl(self, wx.ID_ANY, pos = wx.DefaultPosition, style=wx.TR_HAS_BUTTONS)
#        self.tmpBox = wx.TextCtrl(self, style=wx.TE_MULTILINE)
#        hbox.Add(self.treeDisp, flag=wx.EXPAND|wx.ALL)
#        hbox.Add(self.tmpBox, flag=wx.EXPAND|wx.ALL)
#        vbox.Add(hbox, flag=wx.EXPAND|wx.ALL)
#
#        self.SetSizerAndFit(vbox)


    def OnAbout(self, event):
        """ Displays the About dialog """
        dlg = wx.MessageDialog(self.frame, 'Etymdendron \nAn etymology tree viewer\n'
            'Written 2011 Rich Li','About Etymdendron', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        """ Exits the program """
        self.frame.Close(True)

    def OnLoad(self, event):
        """ Loads the word database """
#TODO: Implement me
        self.dirname = ''
        dlg = wx.FileDialog(self.frame, 'Choose the database file', self.dirname, WORDS_FILE, '*.xml', wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
#            f = open(dlg.GetPath(),'r')
#            self.tmpBox.SetValue(f.read())
#            f.close()
#            dlg2 = wx.MessageDialog(self.frame, "This isn't properly implemented, but I can load the xml file just to show I can do stuff"
#                ,'Error', wx.OK|wx.ICON_EXCLAMATION)
#            dlg2.ShowModal()
#            dlg2.Destroy()
            pass

        dlg.Destroy()

    def OnSave(self, event):
#TODO: Implement me
        """ Saves the word database """
        dlg = wx.MessageDialog(self.frame, 'This function not yet implemented'
            ,'Error', wx.OK|wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()

