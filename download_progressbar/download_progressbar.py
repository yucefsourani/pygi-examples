#!/usr/bin/python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import threading
from urllib import request
import os


class DownloadFile(threading.Thread):
    def __init__(self,progressbar,button,link):
        
        threading.Thread.__init__(self)
        self.progressbar = progressbar
        self.button      = button
        self.link        = link
 
    def run(self):
        GLib.idle_add(self.button.set_sensitive,False)
        try:
            url   = request.Request(self.link,headers={"User-Agent":"Mozilla/5.0"})
            opurl = request.urlopen(url,timeout=10)
            try:
                saveas = opurl.headers["Content-Disposition"].split("=",1)[-1]
            except Exception as e:
                print(e)
                saveas = os.path.basename(opurl.url)
            
            if  os.path.isfile(saveas):
                GLib.idle_add(self.progressbar.set_text,"{} Already Exists".format(saveas))
                GLib.idle_add(self.button.set_sensitive,True)
                return
            else:
                size = int(opurl.headers["Content-Length"])
                psize = 0
                with open(saveas, 'wb') as op:
                    while True:
                        chunk = opurl.read(600)
                        if not chunk:
                            break
                        count = int((psize*100)//size)
                        fraction = count/100
                        op.write(chunk)
                        psize += 600
                        GLib.idle_add(self.progressbar.set_fraction,fraction)
                        GLib.idle_add(self.progressbar.set_text,str(count)+"%")
            
                GLib.idle_add(self.progressbar.set_fraction,1.0)
                GLib.idle_add(self.progressbar.set_text,"Done")
        except Exception as e:
            print(e)
            GLib.idle_add(self.progressbar.set_fraction,0.0)
            GLib.idle_add(self.progressbar.set_text,"Fail")
            GLib.idle_add(self.button.set_sensitive,True)
            return False
            
        GLib.idle_add(self.progressbar.set_fraction,0.0)
        GLib.idle_add(self.button.set_sensitive,True)



class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Download ProgressBar Exmaple")
        self.set_size_request(600, 400)
        
        
        vbox = Gtk.VBox()
        self.add(vbox)

        button = Gtk.Button("Download Learn C Book")
        button.connect("clicked",self.on_button_clicked)
        vbox.pack_start(button,False,False,0)
        
        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_show_text(True)
        vbox.pack_start(self.progressbar,False,False,0)
        
    def on_button_clicked(self,button):
        link = "https://github.com/Hamza5/Learn-to-program-with-C_AR/releases/download/v1.0.1/Learn_C_Language_v1.0.1.pdf"
        DownloadFile(self.progressbar,button,link).start()
        

win = MainWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
