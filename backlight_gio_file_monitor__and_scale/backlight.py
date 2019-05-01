#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  backlight.py
import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gio,GLib,GObject,Gtk
import os
import subprocess
import sys

class BackLightMonitor(GObject.GObject):
    __gsignals__ = {
        "chandeddone"     : (GObject.SignalFlags.RUN_LAST, None, (str,)),
        "canceldone"      : (GObject.SignalFlags.RUN_LAST, None, (bool,)),
        "iscancelled"     : (GObject.SignalFlags.RUN_LAST, None, (bool,)),
        "ratechandeddone" : (GObject.SignalFlags.RUN_LAST, None, (int,))
    }
    def __init__(self,path,rate_limit=800):
        GObject.GObject.__init__(self)
        self.__path         = path
        self.__rate_limit   = rate_limit
        self.__file         = Gio.File.new_for_path(self.__path)
        self.__file_monitor = self.__file.monitor_file(Gio.FileMonitorFlags.NONE)
        self.__file_monitor.set_rate_limit(self.__rate_limit)
        self.__file_monitor.connect("changed",self.__on_changed_)
        
    def __on_changed_(self,file_monitor,file_,other_file,event_type):
        if event_type == Gio.FileMonitorEvent.CHANGES_DONE_HINT:
            with open(self.__path,"r") as mf:
                for line in mf:
                    line = line.strip()
                    if line:
                        self.emit("chandeddone",line)
                        return
    def cancel(self):
        result = self.__file_monitor.cancel()
        self.emit("canceldone",result)
        return result
    
    def is_cancelled(self):
        result = self.__file_monitor.is_cancelled()
        self.emit("iscancelled",result)
        return result
        
    def set_rate_limit(self,rate_limit):
        self.__file_monitor.set_rate_limit(rate_limit)
        self.emit("ratechandeddone",rate_limit)
        return rate_limit


class BackLightMonitorScale(Gtk.Scale):
    def __init__(self,path,
                     rate_limit=800,
                     orientation=0,
                     positiontype=0,
                     initial_value=None,
                     min_value=None,
                     max_value=None,
                     step_increment=None,
                     page_increment=None):
        Gtk.Scale.__init__(self)
        
        self.__path             = path
        self.__rate_limit       = rate_limit
        self.__orientation      = orientation
        self.__positiontype     = positiontype
        self.__initial_value    = initial_value
        self.__min_value        = min_value
        self.__max_value        = max_value
        self.__step_increment   = step_increment
        self.__page_increment   = page_increment
        

        self.__ad1 = self.__init_adjustment()
        self.set_orientation(Gtk.Orientation(self.__orientation))
        self.set_value_pos(Gtk.PositionType(self.__positiontype))
        self.set_adjustment(self.__ad1)
        self.set_vexpand(True)
        self.set_hexpand(True)
        
        
        self.__backlightmonitor         = BackLightMonitor(self.__path,self.__rate_limit)
        self.__backlightmonitor_handler = self.__backlightmonitor.connect("chandeddone",self.__on_changed_)
        
        self.__handler = self.connect("value-changed",self.__on_move_slider)


    def __on_move_slider(self,range_):
        result = int(self.get_value())
        with self.__backlightmonitor.handler_block(self.__backlightmonitor_handler):
            if subprocess.call("echo {} > {}".format(result,os.path.join(os.path.dirname(self.__path),"brightness")),shell=True)!=0:
                self.set_value(self.__old_result)
                return
        self.__old_result = result
        
    def __on_changed_(self,backlightmonitor,result):
        result = int(result)
        with self.handler_block(self.__handler):
            self.set_value(result)
            self.__old_result = result
            

    
    def get_name(self):
        return self.__path.split("/")[-2].split("_",1)[0].title()
        
    def __init_adjustment(self):
        if self.__max_value:
            max_brightness = self.__max_value
        else:
            max_brightness_file = os.path.join(os.path.dirname(self.__path),"max_brightness")
            if os.path.isfile(max_brightness_file):
                with open(max_brightness_file) as mf:
                    max_brightness = mf.read().strip()
                    if max_brightness:
                        max_brightness = int(max_brightness)
                    else:
                        max_brightness = 976
            else:
                max_brightness = 976
                
        
        if self.__initial_value:
            initial_value = self.__initial_value
        else:
            with open(self.__path) as mf:
                initial_value = int(mf.read().strip())
        
        if self.__min_value:
            min_value = self.__min_value
        else:
            min_brightness_file = os.path.join(os.path.dirname(self.__path),"bl_power")
            if os.path.isfile(min_brightness_file):
                with open(min_brightness_file) as mf:
                    min_value = mf.read().strip()
                    if min_value:
                        min_value = int(min_value)
                    else:
                        min_value = 10
            else:
                min_value = 10
            
        if self.__step_increment:
            step_increment = self.__step_increment
        else:
            step_increment = 1
            
        if self.__page_increment:
            page_increment = self.__page_increment
        else:
            page_increment = 10
        self.__old_result = initial_value
        return Gtk.Adjustment.new(initial_value, min_value, max_brightness, step_increment, page_increment, 0)
            

        

    
class WScale(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, 200)
        self.connect("destroy", Gtk.main_quit)
        if len(sys.argv)>1:
            s = BackLightMonitorScale(sys.argv[1])
        else:
            s = BackLightMonitorScale("/sys/class/backlight/intel_backlight/brightness")
        self.add(s)
        print(s.get_name())


window = WScale()
window.show_all()

Gtk.main()
