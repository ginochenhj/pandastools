# I stole most of this from https://gist.github.com/andialbrecht/4463278

import gi
import pandas as pd

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject


class DataFrameTreeModel(GObject.GObject, Gtk.TreeModel, Gtk.TreeSortable):
    def __init__(self, df: pd.DataFrame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df = df
        self.sort_column_id = Gtk.TREE_SORTABLE_UNSORTED_SORT_COLUMN_ID
        self.order = Gtk.SortType.ASCENDING

    def get_column_name(self, column):
        return self.df.columns[column]

    def do_get_iter(self, path: Gtk.TreePath):
        """Returns a new TreeIter that points at path.
        The implementation returns a 2-tuple (bool, TreeIter|None).
        """
        indices = path.get_indices()
        if indices[0] < len(self.df):
            iter_ = Gtk.TreeIter()
            iter_.user_data = indices[0]
            return (True, iter_)
        else:
            return (False, None)

    def do_iter_next(self, iter_):
        """Returns an iter pointing to the next column or None.
        The implementation returns a 2-tuple (bool, TreeIter|None).
        """
        if iter_.user_data is None and len(self.df) != 0:
            iter_.user_data = 0
            return (True, iter_)
        elif iter_.user_data < len(self.df) - 1:
            iter_.user_data += 1
            return (True, iter_)
        else:
            return (False, None)

    def do_iter_has_child(self, iter_: Gtk.TreeIter):
        """True if iter has children."""
        return False

    def do_iter_nth_child(self, iter_: Gtk.TreeIter, n):
        """Return iter that is set to the nth child of iter."""
        # We've got a flat list here, so iter_ is always None and the
        # nth child is the row.
        iter_ = Gtk.TreeIter()
        iter_.user_data = n
        return (True, iter_)

    def do_get_path(self, iter_: Gtk.TreeIter):
        """Returns tree path references by iter."""
        if iter_.user_data is not None:
            path = Gtk.TreePath((iter_.user_data,))
            return path
        else:
            return None

    def do_get_value(self, iter_: Gtk.TreeIter, column):
        """Returns the value for iter and column."""
        return str(self.df.iloc[iter_.user_data, column])

    def do_get_n_columns(self):
        """Returns the number of columns."""
        return len(self.df.columns)

    def do_get_column_type(self, column):
        """Returns the type of the column."""
        # Here we only have strings.
        return str

    def do_get_flags(self):
        """Returns the flags supported by this interface."""
        return Gtk.TreeModelFlags.ITERS_PERSIST, Gtk.TreeModelFlags.LIST_ONLY

    def do_iter_n_children(self, iter_: Gtk.TreeIter):
        return len(self.df) if iter_ is None else 0

    ####################################################################################
    # TreeSortable

    def do_get_sort_column_id(self):
        return (
            0 <= self.sort_column_id,
            self.sort_column_id,
            self.order
        )

    def do_has_default_sort_func(self):
        return False

    def do_set_sort_column_id(self, sort_column_id, order: Gtk.SortType):
        self.sort_column_id = sort_column_id
        self.order = order

        if 0 <= sort_column_id:
            self.df['__index__'] = self.df.index
            self.df.sort_values(self.df.columns[sort_column_id], 0, order is Gtk.SortType.ASCENDING, True)

        self.sort_column_changed()
    
"""
tree_view: Gtk.TreeView =builder.get_object("tree_view")
tree_view.set_model(model.tree_model)

for col in range(model.tree_model.get_n_columns()):
    renderer = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(model.tree_model.get_column_name(col), renderer, text=col)
    column.set_sort_column_id(col)
    tree_view.append_column(column)
"""