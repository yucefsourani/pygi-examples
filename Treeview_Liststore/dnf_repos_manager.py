#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango
import dnf
import subprocess

class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(800,600)
        self.set_border_width(10)
        self.set_title("Dnf Repos Manager")
        
        d = dnf.Base()
        d.read_all_repos()
        
        model = Gtk.ListStore(str,bool)
        for reponame,repo_object in d.repos.items():
            model.append([reponame,repo_object.enabled])
        
        sw = Gtk.ScrolledWindow()
        self.treeview = Gtk.TreeView()
        self.treeview.set_model(model)
        sw.add(self.treeview)
        

        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("editable", False)
        renderer_text.set_property("ellipsize", Pango.EllipsizeMode.END)

        column_text = Gtk.TreeViewColumn("Repo Name", renderer_text, text=0)
        column_text.set_resizable(True)
        column_text.set_fixed_width(400)
        column_text.set_min_width(30)
        self.treeview.append_column(column_text)
        
        renderer_toggled = Gtk.CellRendererToggle()
        renderer_toggled.connect("toggled",self.on_toggled)
        renderer_toggled.set_alignment(0,0)
        column_toggled = Gtk.TreeViewColumn("Status", renderer_toggled, active=1)
        self.treeview.append_column(column_toggled)
        
        self.add(sw)

    def on_toggled(self,cell_renderer_toggle, path):
        model = self.treeview.get_model()
        iter_ = model.get_iter(path)
        repo_name , isenabled = model[iter_]
        if isenabled:
            check = subprocess.call("pkexec dnf config-manager --set-disabled {}".format(repo_name),shell=True)
        else:
            check = subprocess.call("pkexec dnf config-manager --set-enabled {}".format(repo_name),shell=True)
        
        if check == 0:
            model[iter_] = [repo_name,not isenabled ]
        return True
        
win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
