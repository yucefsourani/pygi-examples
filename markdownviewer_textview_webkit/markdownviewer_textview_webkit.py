#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  markdownviewer_textview_webkit.py
#  
#  Copyright 2018 youcef sourani <youssef.m.sourani@gmail.com>

import gi
gi.require_version('WebKit2', '4.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import WebKit2
import markdown2


def convert_markdown_to_html(markdown_text,extra=None):
    """
    Convert from markdown to html .
    """
    if not extra:
        extra = ["cuddled-lists","code-friendly","fenced-code-blocks"] #https://github.com/trentm/python-markdown2/wiki/Extras
    return markdown2.markdown(markdown_text,extras=extra)


def on_text_buffer_changed(textbuffer,webview):
    """
    1-Get all text from textview.
    2-Convert text to html.
    3-Load html text in webview.
    """
    text = textbuffer.get_text(textbuffer.get_start_iter(),textbuffer.get_end_iter(),False) # get all text from textview
    html_text = convert_markdown_to_html(text) # convert text to html
    webview.load_html(html_text) # load html text in webview


def program_gui_run():
    # make window
    window = Gtk.Window()
    window.maximize()
    vbox = Gtk.VBox(spacing=10)


    # make webview widget and load html text
    webview = WebKit2.WebView()
    #webview.load_html(html_text)

    # make scrolled window for webview
    webview_scrolled_window = Gtk.ScrolledWindow()
    webview_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    webview_scrolled_window.add(webview)

    # make webview widget and load html text
    textview    = Gtk.TextView()
    textview.set_wrap_mode(Gtk.WrapMode(3))
    text_buffer = textview.get_buffer()
    text_buffer.connect("changed",on_text_buffer_changed,webview)


    # make scrolled window for textview
    textview_scrolled_window = Gtk.ScrolledWindow()
    textview_scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
    textview_scrolled_window.add(textview)

    # Vertical Separator
    vs = Gtk.VSeparator()
    
    vbox.pack_start(textview_scrolled_window,True,True,0)
    vbox.pack_start(vs,False,True,0)
    vbox.pack_start(webview_scrolled_window,True,True,0)
    window.add(vbox)
    window.connect("delete-event", Gtk.main_quit) 
    window.show_all()                            
    Gtk.main()                                    

if __name__ =="__main__":
    program_gui_run()
