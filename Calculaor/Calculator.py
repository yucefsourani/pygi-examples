# Copyright (C) 2017 amine
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi
from math import *
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk,Gio

MENU_XML="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <menu id="app-menu">
        <section>
            <item>
                <attribute name="action">app.about</attribute>
                <attribute name="label" translatable="yes">_About</attribute>
            </item>
            <item>
                <attribute name="action">app.quit</attribute>
                <attribute name="label" translatable="yes">_Quit</attribute>
            </item>
        </section>
    </menu>
</interface>
"""

class Application(Gtk.Application):

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.about_click)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)


        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))

        
    def do_activate(self):
        global window
        window = Gtk.ApplicationWindow.new(self)
        window.set_border_width(10)
        window.set_resizable(False)
        window.set_position(Gtk.WindowPosition.CENTER)
        window.set_icon_name("accessories-calculator")
        window.set_title('amine')
        hb=Gtk.HeaderBar()
        hb.set_show_close_button(True)
        window.set_titlebar(hb)

        


        stack=Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(1000)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(stack)
        hb.set_custom_title(stack_switcher)
        window.add(stack)

        global clipboard
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        

        #Scientific
        button1 = Gtk.Button(label="1")
        button2 = Gtk.Button(label="2")
        button3 = Gtk.Button(label="3")
        button4 = Gtk.Button(label="4")
        button5 = Gtk.Button(label="5")
        button6 = Gtk.Button(label="6")
        button7 = Gtk.Button(label="7")
        button8 = Gtk.Button(label="8")
        button9 = Gtk.Button(label="9")
        button10 = Gtk.Button(label="0")
        button11 = Gtk.Button(label=".")
        button12 = Gtk.Button(label="/")
        button13 = Gtk.Button(label="(")
        button14 = Gtk.Button(label="-")
        button15 = Gtk.Button(label="+")
        button16 = Gtk.Button(label="*")
        button17 = Gtk.Button(label=")")
        button18 = Gtk.Button(label="tan")
        button19 = Gtk.Button(label="sin")
        button20 = Gtk.Button(label="cos")
        button21 = Gtk.Button(label="π")
        button22 = Gtk.Button(label="tanh")
        button23 = Gtk.Button(label="sinh")
        button24 = Gtk.Button(label="cosh")
        button25 = Gtk.Button(label="e")
        button26 = Gtk.Button(label="exp")
        button27 = Gtk.Button(label="log")
        button28 = Gtk.Button(label="ans")
        button = Gtk.Button(label="=")
        button.get_style_context().add_class("suggested-action")
        remove_button=Gtk.Button()
        i=Gtk.Image.new_from_icon_name("edit-clear-symbolic",Gtk.IconSize.BUTTON)
        remove_button.set_image(i)
        copy_button=Gtk.Button()
        j=Gtk.Image.new_from_icon_name("edit-copy-symbolic",Gtk.IconSize.BUTTON)
        copy_button.set_image(j)

        

        entry=Gtk.Entry()
        global entrybuffer
        entrybuffer = Gtk.EntryBuffer()
        entry.set_buffer(entrybuffer)

        global label
        label=Gtk.Label()

        table1=Gtk.Table(6,7,True)
        table1.set_row_spacing(0,5)
        table1.set_row_spacing(1,5)
        table1.set_row_spacing(2,5)
        table1.set_row_spacing(3,5)
        table1.set_row_spacing(4,5)
        table1.set_col_spacing(0,5)
        table1.set_col_spacing(1,5)
        table1.set_col_spacing(2,10)
        table1.set_col_spacing(3,5)
        table1.set_col_spacing(4,5)
        table1.set_col_spacing(5,5)
        table1.attach(button1,0,1,0,1)
        table1.attach(button2,1,2,0,1)
        table1.attach(button3,2,3,0,1)
        table1.attach(button4,0,1,1,2)
        table1.attach(button5,1,2,1,2)
        table1.attach(button6,2,3,1,2)
        table1.attach(button7,0,1,2,3)
        table1.attach(button8,1,2,2,3)
        table1.attach(button9,2,3,2,3)
        table1.attach(button10,0,1,3,4)
        table1.attach(button11,1,2,3,4)
        table1.attach(button12,2,3,3,4)
        table1.attach(button13,3,4,0,1)
        table1.attach(button14,3,4,1,2)
        table1.attach(button15,3,4,2,3)
        table1.attach(button16,3,4,3,4)
        table1.attach(button17,4,5,0,1)
        table1.attach(button18,4,5,1,2)
        table1.attach(button19,4,5,2,3)
        table1.attach(button20,4,5,3,4)
        table1.attach(button21,5,6,0,1)
        table1.attach(button22,5,6,1,2)
        table1.attach(button23,5,6,2,3)
        table1.attach(button24,5,6,3,4)
        table1.attach(button25,6,7,0,1)
        table1.attach(button26,6,7,1,2)
        table1.attach(button27,6,7,2,3)
        table1.attach(button28,6,7,3,4)
        table1.attach(entry,0,6,4,5)
        table1.attach(button,0,2,5,6)
        table1.attach(label,2,6,5,6)
        table1.attach(remove_button,6,7,4,5)
        table1.attach(copy_button,6,7,5,6)



        button1.connect("clicked",self.button_1)
        button2.connect("clicked",self.button_2)
        button3.connect("clicked",self.button_3)
        button4.connect("clicked",self.button_4)
        button5.connect("clicked",self.button_5)
        button6.connect("clicked",self.button_6)
        button7.connect("clicked",self.button_7)
        button8.connect("clicked",self.button_8)
        button9.connect("clicked",self.button_9)
        button10.connect("clicked",self.button_10)
        button11.connect("clicked",self.button_11)
        button12.connect("clicked",self.button_12)
        button13.connect("clicked",self.button_13)
        button14.connect("clicked",self.button_14)
        button15.connect("clicked",self.button_15)
        button16.connect("clicked",self.button_16)
        button17.connect("clicked",self.button_17)
        button18.connect("clicked",self.button_18)
        button19.connect("clicked",self.button_19)
        button20.connect("clicked",self.button_20)
        button21.connect("clicked",self.button_21)
        button22.connect("clicked",self.button_22)
        button23.connect("clicked",self.button_23)
        button24.connect("clicked",self.button_24)
        button25.connect("clicked",self.button_25)
        button26.connect("clicked",self.button_26)
        button27.connect("clicked",self.button_27)
        button28.connect("clicked",self.button_28)
        remove_button.connect("clicked",self.removebutton)
        copy_button.connect("clicked",self.copybutton)
        button.connect('clicked',self.button)


        stack.add_titled(table1,"scientific","Scientific")


        #History
        global liststore
        liststore = Gtk.ListStore(str, str)
        treeview = Gtk.TreeView(model=liststore)
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("calcul                             ", renderer_text, text=0)
        treeview.append_column(column_text)
        renderer_editabletext = Gtk.CellRendererText()
        renderer_editabletext.set_property("editable", True)
        column_editabletext = Gtk.TreeViewColumn("Result",renderer_editabletext, text=1)
        treeview.append_column(column_editabletext)
        scrolled = Gtk.ScrolledWindow()
        scrolled.add(treeview)
        stack.add_titled(scrolled,"historique","History")

        #App_menu
        


        #Equation
        pbutton=Gtk.ToolButton(label="Equation")
        pbutton.connect('clicked',self.on_popover_clicked)
        self.popover = Gtk.Popover()
        self.popover.set_position(Gtk.PositionType.TOP)
        self.popover.set_relative_to(pbutton)
        table2=Gtk.Table(6,5,True)
        self.popover.add(table2)
        label2 = Gtk.Label("ax²+bx+c=0")
        labela=Gtk.Label("a:")
        labelb=Gtk.Label("b:")
        labelc=Gtk.Label("c:")
        global labelr
        labelr=Gtk.Label()
        global entrya
        entrya=Gtk.Entry()
        global entryb
        entryb=Gtk.Entry()
        global entryc
        entryc=Gtk.Entry()
        buttonr=Gtk.Button(label="result")
        buttonr.get_style_context().add_class("suggested-action")
        buttonr.connect('clicked',self.eq_result)
        table2.attach(label2,0,5,0,1)
        table2.attach(labela,0,1,1,2)
        table2.attach(labelb,0,1,2,3)
        table2.attach(labelc,0,1,3,4)
        table2.attach(labelr,0,5,5,6)
        table2.attach(entrya,1,5,1,2)
        table2.attach(entryb,1,5,2,3)
        table2.attach(entryc,1,5,3,4)
        table2.attach(buttonr,1,4,4,5)
        table2.set_row_spacing(1,3)
        table2.set_row_spacing(2,3)
        table2.set_row_spacing(3,3)
        hb.pack_start(pbutton)

        #window.connect("delete-event", Gtk.main_quit)
        window.show_all()


    def eq_result(self,NULL):
        a=entrya.get_text()
        if a=='':
            a=0
        else:
            a=float(a)
        b=entryb.get_text()
        if b=='':
            b=0
        else:
            b=float(b)
        c=entryc.get_text()
        if c=='':
            c=0
        else:
            c=float(c)
        
        r=equation(a,b,c)
        labelr.set_text(r)

    def button(self,NULL):
        #global ans
        ans=label.get_text()
        if ans != '':
            ans=float(ans)
        π=pi
        a=entrybuffer.get_text()
        b=a
        a=eval(a)
        label.set_text(str(a))
        liststore.append([b, str(a)])

    def button_1(self,NULL):
        entrybuffer.insert_text(1000,'1',-1)

    def button_2(self,NULL):
        entrybuffer.insert_text(1000,'2',-1)

    def button_3(self,NULL):
        entrybuffer.insert_text(1000,'3',-1)

    def button_4(self,NULL):
        entrybuffer.insert_text(1000,'4',-1)

    def button_5(self,NULL):
        entrybuffer.insert_text(1000,'5',-1)

    def button_6(self,NULL):
        entrybuffer.insert_text(1000,'6',-1)

    def button_7(self,NULL):
        entrybuffer.insert_text(1000,'7',-1)

    def button_8(self,NULL):
        entrybuffer.insert_text(1000,'8',-1)

    def button_9(self,NULL):
        entrybuffer.insert_text(1000,'9',-1)

    def button_10(self,NULL):
        entrybuffer.insert_text(1000,'0',-1)

    def button_11(self,NULL):
        entrybuffer.insert_text(1000,'.',-1)

    def button_12(self,NULL):
        entrybuffer.insert_text(1000,'/',-1)

    def button_13(self,NULL):
        entrybuffer.insert_text(1000,'(',-1)

    def button_14(self,NULL):
        entrybuffer.insert_text(1000,'-',-1)

    def button_15(self,NULL):
        entrybuffer.insert_text(1000,'+',-1)

    def button_16(self,NULL):
        entrybuffer.insert_text(1000,'*',-1)

    def button_17(self,NULL):
        entrybuffer.insert_text(1000,')',-1)

    def button_18(self,NULL):
        entrybuffer.insert_text(1000,'tan(',-1)

    def button_19(self,NULL):
        entrybuffer.insert_text(1000,'sin(',-1)

    def button_20(self,NULL):
        entrybuffer.insert_text(1000,'cos(',-1)

    def button_21(self,NULL):
        entrybuffer.insert_text(1000,'π',-1)

    def button_22(self,NULL):
        entrybuffer.insert_text(1000,'tanh(',-1)

    def button_23(self,NULL):
        entrybuffer.insert_text(1000,'sinh(',-1)

    def button_24(self,NULL):
        entrybuffer.insert_text(1000,'cosh(',-1)

    def button_25(self,NULL):
        entrybuffer.insert_text(1000,'e',-1)

    def button_26(self,NULL):
        entrybuffer.insert_text(1000,'exp(',-1)

    def button_27(self,NULL):
        entrybuffer.insert_text(1000,'log(',-1)

    def button_28(self,NULL):
        entrybuffer.insert_text(1000,'ans',-1)

    def removebutton(self,NULL):
        entrybuffer.delete_text(0,-1)

    def copybutton(self,widget):
        clipboard.set_text(label.get_text(), -1)

    def about_close(self,about):
        self.about.close()
        self.about.destroy()

    def on_popover_clicked(self, button):
        self.popover.show_all()

    def on_quit(self, action, param):
        sys.exit(self.run(sys.argv))

    def about_click(self,action, param):
        self.about=Gtk.AboutDialog(modal=True)
        self.about.set_transient_for(window)
        self.about.set_program_name('Calculator')
        self.about.set_version('1.0')
        self.about.set_copyright('Calculator programming with python')
        self.about.set_website('aminenet.weebly.com')
        self.about.set_logo_icon_name("accessories-calculator")
        self.about.set_authors(["Mohamed Amine Bouzidi"])
        self.about.set_license("""Calculator is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

Calculatorl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Calculator.  If not, see <http://www.gnu.org/licenses/>.""")
        self.about.run()
        self.about.destroy()


def equation(a,b,c):
   if a==0:
        if b==0:
            r="no solution"
        else:
            x=-(c/b)
            r=str(x)
   else:
      delta=b*b-4*a*c
      if delta>0:
         x1=(-b-sqrt(delta))/2*a
         x2=(-b+sqrt(delta))/2*a
         r=str(x1)[0:8]+"  and  "+str(x2)[0:8]
      if delta==0:
         x=-b/2*a
         r=str(x)
      if delta<0:
         r="no solution"
   return r


def main():
    application = Application()

    try:
        ret = application.run(sys.argv)
    except SystemExit as e:
        ret = e.code

    sys.exit(ret)

if __name__ == '__main__':
    main()

