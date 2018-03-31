#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#  arfedora-terminal.py
#  
#  Copyright 2018 youcef sourani <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
import os
import pwd
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte, GLib, Gdk


class CursorShape(Gtk.Dialog):
    def __init__(self,parent,terminal):
        Gtk.Dialog.__init__(self,parent=parent)
        self.set_modal(True)
        self.set_title("Cursor Shape") #cursor_shape

        self.parent = parent
        self.terminal = terminal
        parent_size = self.parent.get_size()
        width  = parent_size[0]
        height = parent_size[1]
        self.set_default_size(width/2 if width>600 else 300, height/2 if height>400 else 200)
        self.add_button("_OK", Gtk.ResponseType.OK)
        self.connect("response", self.on_response)

        label = Gtk.Label("Change Cursor Shape")
        self.vbox.pack_start(label,True,True,0)


        radiobutton1 = Gtk.RadioButton(label="Block")
        self.vbox.pack_start(radiobutton1, True, True, 0)
        
        radiobutton2 = Gtk.RadioButton(label="Ibeam ", group=radiobutton1)
        
        self.vbox.pack_start(radiobutton2, True, True, 0)
        
        radiobutton3 = Gtk.RadioButton(label="Under Line", group=radiobutton1)
        self.vbox.pack_start(radiobutton3, True, True, 0)
        
        if self.terminal.get_cursor_shape()==0:
            radiobutton1.set_active(True)
        elif self.terminal.get_cursor_shape()==1:
            radiobutton2.set_active(True)
        else:
            radiobutton3.set_active(True)
            
        radiobutton1.connect("toggled", self.on_radio_button_toggled,0)
        radiobutton2.connect("toggled", self.on_radio_button_toggled,1)
        radiobutton3.connect("toggled", self.on_radio_button_toggled,2)
        
        self.show_all()

    def on_radio_button_toggled(self,b,data):
        self.terminal.set_cursor_shape(Vte.CursorShape(data))
        
    def on_response(self, dialog, response):
        dialog.destroy()


class FontChange(Gtk.FontChooserDialog):
    def __init__(self,parent,terminal):
        Gtk.FontChooserDialog.__init__(self,parent=parent)
        self.set_title("FontChooserDialog")
        self.terminal = terminal
        
        response = self.run()
        if response == Gtk.ResponseType.OK:
            self.terminal.set_font(self.get_font_desc())
        
        self.destroy()
    

        
        
class Terminal(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ArFedora Terminal")
        self.resize(800, 400)
        scrolledwindow = Gtk.ScrolledWindow()
        self.add(scrolledwindow)
        
        self.terminal = Vte.Terminal()
        self.terminal.connect("eof",self.quit_)
        self.terminal.set_color_background(Gdk.RGBA(red=0.180392, green=0.203922, blue=0.211765, alpha=1.000000))
        self.terminal.set_color_foreground(Gdk.RGBA(red=0.988235, green=0.913725, blue=0.309804, alpha=1.000000))
        self.terminal.set_allow_hyperlink(True)
        
        vadjustment = self.terminal.get_vadjustment()
        scrolledwindow.set_vadjustment(vadjustment)

        user_info = pwd.getpwuid(os.geteuid())
        self.terminal.spawn_sync(
                        Vte.PtyFlags.DEFAULT,
                        user_info.pw_dir,
                        [user_info.pw_shell],
                        [],
                        GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                        None,
                        None
                        )
        
        
        self.terminal.connect("button-release-event",self.on_button_event)
        self.menu = Gtk.Menu()
        self.menu.set_screen(Gdk.Screen().get_default())
        
        copytextmenuitem = Gtk.MenuItem("Copy")
        pastetextmenuitem = Gtk.MenuItem("Paste")
        fontsizemenuitem = Gtk.MenuItem("Font")
        cursorshapemenuitem = Gtk.MenuItem("Cursor Shape")
        cursorcolormenuitem = Gtk.MenuItem("Cursor Color")
        backgroundmenuitem = Gtk.MenuItem("Backgound Color")
        foregroundmenuitem = Gtk.MenuItem("Foreground Color")
        
        copytextmenuitem.connect("activate", self.copy_text)
        pastetextmenuitem.connect("activate", self.paste_text)
        fontsizemenuitem.connect("activate", self.font_change)
        cursorshapemenuitem.connect("activate", self.cursor_shape)
        cursorcolormenuitem.connect("activate", self.on_cursor_menuitem_activated)
        backgroundmenuitem.connect("activate", self.on_background_menuitem_activated)
        foregroundmenuitem.connect("activate", self.on_foreground_menuitem_activated)
        
        self.menu.append(copytextmenuitem)
        self.menu.append(pastetextmenuitem)
        self.menu.append(fontsizemenuitem)
        self.menu.append(cursorshapemenuitem)
        self.menu.append(cursorcolormenuitem)
        self.menu.append(backgroundmenuitem)
        self.menu.append(foregroundmenuitem)
        scrolledwindow.add(self.terminal)

    def copy_text(self,w):
        self.terminal.copy_clipboard()
        
    def paste_text(self,w):
        self.terminal.paste_clipboard()

    def font_change(self,w):
        FontChange(self,self.terminal)
        
    def cursor_shape(self,w):
        CursorShape(self,self.terminal)
        
    def on_button_event(self,terminal,event):
        if  event.button==3:
            self.menu.popup_at_pointer()
            self.menu.show_all()

    def on_cursor_menuitem_activated(self,menuitem):
        colorchooserdialog = Gtk.ColorChooserDialog(parent=self)
        if colorchooserdialog.run() == Gtk.ResponseType.OK:
            color = colorchooserdialog.get_rgba()
            self.terminal.set_color_cursor(color)
        colorchooserdialog.destroy()
        
        
    def on_background_menuitem_activated(self,menuitem):
        colorchooserdialog = Gtk.ColorChooserDialog(parent=self)
        if colorchooserdialog.run() == Gtk.ResponseType.OK:
            color = colorchooserdialog.get_rgba()
            self.terminal.set_color_background(color)
        colorchooserdialog.destroy()

    def on_foreground_menuitem_activated(self,menuitem):
        colorchooserdialog = Gtk.ColorChooserDialog(parent=self)
        if colorchooserdialog.run() == Gtk.ResponseType.OK:
            color = colorchooserdialog.get_rgba()
            self.terminal.set_color_foreground(color)
        colorchooserdialog.destroy()
        
        
    def quit_(self,w):
        Gtk.main_quit()
        
terminal = Terminal()
terminal.connect("delete-event", Gtk.main_quit)
terminal.show_all()
Gtk.main()
