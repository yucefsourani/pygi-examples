#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Password Entry Exmaple")
        self.set_size_request(200, 100)
        
        
        vbox = Gtk.VBox()
        self.add(vbox)
        
        self.icon_show =  GdkPixbuf.Pixbuf.new_from_file("icons/130516.svg")
        self.icon_hide = GdkPixbuf.Pixbuf.new_from_file("icons/132906.svg")
        #self.icon_show = GdkPixbuf.Pixbuf.new_from_file_at_size("130516.svg",32,32)
        #self.icon_hide = GdkPixbuf.Pixbuf.new_from_file_at_size("132906.svg",32,32)

        
        self.entry = Gtk.Entry()
        
        self.entry.set_visibility(False)
        vbox.pack_start(self.entry, True, True, 0)
        self.entry.connect("icon-press",self.on_icon_press)
        self.entry.props.secondary_icon_tooltip_markup = "<b>Show Password</b>"
        self.entry.props.secondary_icon_pixbuf = self.icon_show
        
        button = Gtk.Button("Print Text")
        vbox.pack_start(button, True, True, 0)
        button.connect("clicked",self.on_button_clicked)
        
    def on_icon_press(self, entry,icon_position,event):
        if event.type == Gdk.EventType.BUTTON_PRESS and event.button==1:
            if entry.get_visibility():
                entry.set_visibility(False)
                entry.props.secondary_icon_tooltip_markup = "<b>Show Password</b>"
                entry.props.secondary_icon_pixbuf = self.icon_show
            else:
                entry.set_visibility(True)
                entry.props.secondary_icon_tooltip_markup = "<b>Hide Password</b>"
                entry.props.secondary_icon_pixbuf = self.icon_hide

    def on_button_clicked(self,button):
        text = self.entry.get_text()
        if text:
            print(self.entry.get_text())

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
