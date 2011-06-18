#!/usr/bin/env python
"""This module launches the GUI for etymdendron"""

import wx
import gui_funcs


def main():
    # Create and show the frame
    app = gui_funcs.EtymApp(True)
    app.MainLoop()

if __name__ == '__main__':
    main()
