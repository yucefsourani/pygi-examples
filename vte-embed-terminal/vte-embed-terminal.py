#!/usr/bin/python3
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Vte, GLib, Gdk

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Embed Terminal")
        self.resize(975, 645)
        
        
        vbox = Gtk.VBox(spacing=20)
        self.add(vbox)
        
        button = Gtk.Button("Show Embed Terminal")
        button.connect("clicked",self.on_button_clicked)
        vbox.pack_start(button,False,False,0)
        
        
        self.revealer = Gtk.Revealer()
        self.revealer.set_reveal_child(False)
        vbox.pack_start(self.revealer,False,False,0)
        
        
        self.terminal = Vte.Terminal()
        #self.terminal.set_color_background(Gdk.RGBA (0.5,1.0,0.0,2))
        #self.terminal.set_opacity(0.4)
        self.terminal.set_size_request(200, 200)
        self.terminal.spawn_sync(
                        Vte.PtyFlags.DEFAULT,
                        os.environ['HOME'],
                        ["/bin/bash"],
                        [],
                        GLib.SpawnFlags.DO_NOT_REAP_CHILD,
                        None,
                        None
                        )
        self.revealer.add(self.terminal)
                        


    def on_button_clicked(self,button):
        if self.revealer.get_reveal_child():
            self.revealer.set_reveal_child(False)
            button.set_label("Show Embed Terminal")
        else:
            self.revealer.set_reveal_child(True)
            button.set_label("Hide Embed Terminal")
            
        
win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
