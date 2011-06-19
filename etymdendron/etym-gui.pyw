#!/usr/bin/env python
"""This module launches the GUI for etymdendron"""

import gui_funcs

def main():
    # Create and show the app
    app = gui_funcs.EtymApp(False)
    # Load in the default XML file
    app.LoadWordDB()
    # Run it
    app.MainLoop()

if __name__ == '__main__':
    main()
