"""
Class definition for HomeWindow
"""

from kivy.uix.screenmanager import Screen
import os
import webbrowser
import widgets.HomeWindowWidget
from os.path import dirname, join, normpath


class HomeWindow(Screen):
    """
    Login screen
    """

    def open_documentation(self):
        curdir = dirname(__file__)
        filename = join(curdir, 'resources')
        filename = join(filename, 'pdfs')
        filename = join(filename, 'Electrical%20Build.pdf')
        filename = filename + ""
        filename = filename.replace("\\", "/")
        print(filename)
        webbrowser.open("file:///" + filename)

    def open_projectinfo(self, weblink):
        webbrowser.open(weblink)
