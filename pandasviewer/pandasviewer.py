#import
import pandas as pd
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from DataFrameTreeModel import DataFrameTreeModel

class PandasColumnProperties:
    def __init__(self, name, dtype) -> None:
        self.name, self.dtype = name, dtype
        
class PandasViewer(Gtk.Window):
    def __init__(self, df):
        Gtk.Window.__init__(self, title="PandasViewer")


        # Create the ListStore model
        self.model = DataFrameTreeModel(df)

        self.treeview = Gtk.TreeView(self.model)
        self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
        for col in range(self.model.get_n_columns()):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(self.model.get_column_name(col), renderer, text=col)
            column.set_sort_column_id(col)
            self.treeview.append_column(column)
        self.scrolled_treeview = Gtk.ScrolledWindow()
        self.scrolled_treeview.set_border_width(10)
        self.scrolled_treeview.set_vexpand(True)
        self.scrolled_treeview.add(self.treeview)


        # Create a layout
        self.vbox = Gtk.VBox(spacing=2, homogeneous=False)
        # Place TreeView inside the layout
        self.vbox.pack_start(self.scrolled_treeview, False, True, 0)
        self.add(self.vbox)
        # self.show()

def show_dataframe(df):
    win = PandasViewer(df)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.resize(1024, 768)

    Gtk.main()
