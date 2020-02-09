#!/usr/bin/env python 
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from main import MainWindow
import os

if __name__ == "__main__":
    # Suppress GTK Warnings
    os.environ['G_ENABLE_DIAGNOSTIC'] = "0"
    app = MainWindow()
    app.window.show_all()
    Gtk.main()

