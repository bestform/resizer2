#!/usr/bin/env python

import gtk, os

path_to_presets = "presets.cfg"

class Resizer2(object):
    def __init__(self):
        builder = gtk.Builder()
        builder.add_from_file("resizer2.glade")
        dic = {"on_Resizer2_destroy" : gtk.main_quit,
               "on_treeview1_row_activated" : self.on_treeview1_row_activated,
               "on_resizeBtn_clicked" : self.on_resizeBtn_clicked
               }
        

        builder.connect_signals(dic)

        self.widthBtn = builder.get_object("widthBtn")
        self.heightBtn = builder.get_object("heightBtn")
        self.fill_presets(builder.get_object("treeview1"))
        builder.get_object("Resizer2").show()

    def fill_presets(self, treeview):
        self.treestore = gtk.TreeStore(str)
        first = False
        for i in open(path_to_presets):
            value = i.strip('\n ')
            if not first:
                first = True
                self.set_value(value)
            self.treestore.append(None, [value])
        treeview.set_model(self.treestore)
        tvcolumn = gtk.TreeViewColumn("Presets")
        treeview.append_column(tvcolumn)
        cell = gtk.CellRendererText()
        tvcolumn.pack_start(cell, True)
        tvcolumn.add_attribute(cell, 'text', 0)
        
    def on_treeview1_row_activated(self, widget, position, column):
        entry1, entry2 = widget.get_selection().get_selected()
        entry = entry1.get_value(entry2, 0)
        self.set_value(entry)

    def set_value(self, value):
        w, h = value.split("x")
        if h:
            self.widthBtn.set_value(float(w))
            self.heightBtn.set_value(float(h))

    def on_resizeBtn_clicked(self, widget):
        w = self.widthBtn.get_value()
        h = self.heightBtn.get_value()
        command = "wmctrl -r :SELECT: -e 0,-1,-1,%i,%i"%(w,h)
        os.system(command)

if __name__ == "__main__":
    app = Resizer2()
    gtk.main()
