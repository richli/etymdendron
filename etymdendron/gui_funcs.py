#!/usr/bin/env python
""" This module contains classes and such needed for the GUI """

# We're using wxWidgets as a cross-platform toolkit
import os
import wx
from global_opts import WORDS_FILE

# Define the main frame
class EtymFrame(wx.Frame):
    """ Our subclass implementation of Frame """
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(400,300))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        #self.CreateStatusBar()

        # Create the menus
        fileMenu = wx.Menu()
        helpMenu = wx.Menu()
        menuLoad = fileMenu.Append(wx.ID_ANY,'&Load', 'Load the database file')
        menuSave = fileMenu.Append(wx.ID_ANY,'&Save', 'Save the database file')
        fileMenu.AppendSeparator()
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "End the program")
        menuAbout = helpMenu.Append(wx.ID_ABOUT, "&About", "Information about the program")

        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,"&File")
        menuBar.Append(helpMenu,"&Help")
        self.SetMenuBar(menuBar)

        # Define menu bindings
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnLoad, menuLoad)
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)

        self.Show(True)

    def OnAbout(self, event):
        """ Displays the About dialog """
        dlg = wx.MessageDialog(self, 'Etymdendron \nAn etymology tree viewer\n'
            'Written 2011 Rich Li','About Etymdendron', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        """ Exits the program """
        self.Close(True)

    def OnLoad(self, event):
        """ Loads the word database """
#TODO: Implement me
        self.dirname = ''
        dlg = wx.FileDialog(self, 'Choose the database file', self.dirname, WORDS_FILE, '*.xml', wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            print('yup')
        dlg.Destroy()

    def OnSave(self, event):
#TODO: Implement me
        """ Saves the word database """
        dlg = wx.MessageDialog(self, 'This function not yet implemented'
            ,'Error', wx.OK|wx.ICON_EXCLAMATION)
        dlg.ShowModal()
        dlg.Destroy()

