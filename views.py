from gi.repository import Gtk, GObject, Gdk
from constants import Status
import resources
from print_pretty.pretty_size import psize



def status_size_data_func(tree_column, cell, tree_model, iter, data):
    size = tree_model[iter][3]
    cell.set_property('text', psize(size))
    
def status_cell_data_func(tree_column, cell, tree_model, iter, data):
    status = tree_model[iter][1]
    if status == Status.ACTIVE:
        cell.set_property('pixbuf', resources.active_pixbuf)
    elif status == Status.SLEEP:
        cell.set_property('pixbuf', None)
    elif status == Status.QUEUED:
        cell.set_property('pixbuf', resources.queued_pixbuf)
    elif status == Status.SOLVING:
        cell.set_property('pixbuf', resources.solving)
    elif status == Status.DOWNLOAD:
        cell.set_property('pixbuf', resources.download_pixbuf)
    elif status == Status.ERROR:
        cell.set_property('pixbuf', resources.error)


class IconView(Gtk.FlowBox):
    # __gsignals__ = {
    #   'scope-changed': (GObject.SIGNAL_RUN_FIRST, None, ()),
    # }
    def __init__(self, menu):
        Gtk.FlowBox.__init__(self)

        self.menu = menu


        # self.get_selection().set_mode(0)
        # # downview.set_rubber_banding(True)
        # self.set_property('headers-visible', False)

        # column = Gtk.TreeViewColumn('id')
        # renderer = Gtk.CellRendererText()
        # column.pack_start(renderer, False)
        # column.add_attribute(renderer, 'text', 0)
        # self.append_column(column)

        # column = Gtk.TreeViewColumn('status')
        # renderer = Gtk.CellRendererPixbuf()
        # column.pack_start(renderer, False)
        # column.set_cell_data_func(renderer, status_cell_data_func, func_data=None)
        # self.append_column(column)

        # column = Gtk.TreeViewColumn('progress')
        # column.set_fixed_width(120)
        # renderer = Gtk.CellRendererProgress()
        # column.pack_start(renderer, False)
        # column.add_attribute(renderer, 'value', 2)
        # self.append_column(column)

        # column = Gtk.TreeViewColumn('size')
        # renderer = Gtk.CellRendererText()
        # column.pack_start(renderer, False)
        # column.set_cell_data_func(renderer, status_size_data_func, func_data=None)
        # # column.add_attribute(renderer, 'text', 3)
        # self.append_column(column)

        # column = Gtk.TreeViewColumn('host')
        # renderer = Gtk.CellRendererText()
        # column.pack_start(renderer, False)
        # column.add_attribute(renderer, 'text', 5)
        # self.append_column(column)

        # column = Gtk.TreeViewColumn('set')
        # renderer = Gtk.CellRendererText()
        # column.pack_start(renderer, True)
        # column.add_attribute(renderer, 'text', 4)
        # self.append_column(column)


class SetWindow(Gtk.TreeView):
    # __gsignals__ = {
    #   'scope-changed': (GObject.SIGNAL_RUN_FIRST, None, ()),
    # }
    def __init__(self, menu):
        Gtk.TreeView.__init__(self)

        self.menu = menu

        self.get_selection().set_mode(3)
        self.set_rubber_banding(True)

        column = Gtk.TreeViewColumn('id')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, False)
        column.add_attribute(renderer, 'text', 0)
        self.append_column(column)

        column = Gtk.TreeViewColumn('status')
        renderer = Gtk.CellRendererPixbuf()
        column.pack_start(renderer, False)
        # column.add_attribute(renderer, 'text', 1)
        column.set_cell_data_func(renderer, status_cell_data_func, func_data=None)
        self.append_column(column)

        column = Gtk.TreeViewColumn('count')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, False)
        column.add_attribute(renderer, 'text', 2)
        self.append_column(column)

        column = Gtk.TreeViewColumn('set')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 3)
        self.append_column(column)

        column = Gtk.TreeViewColumn('host')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, False)
        column.add_attribute(renderer, 'text', 4)
        self.append_column(column)


    def do_button_press_event(self, event):
        if event.button == Gdk.BUTTON_SECONDARY:
            selection = self.get_selection()
            pos = self.get_path_at_pos(event.x, event.y)# path, column, cell_x, cell_y
            if pos:
                #clicked any content
                path, column, cell_x, cell_y = pos
                if selection.path_is_selected(path):
                    #clicked in selection
                    self.menu.popup(None, None, None, None, event.button, event.time)
                else:
                    #clicked outside of selection
                    Gtk.TreeView.do_button_press_event(self, event)
                    self.menu.popup(None, None, None, None, event.button, event.time)
            else:
                #clicked empty area
                selection.unselect_all()
                return False
        else:
            Gtk.TreeView.do_button_press_event(self, event)