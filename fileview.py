from gi.repository import Gtk, GObject, Gdk
from print_pretty.pretty_size import psize
from stores import ViewStore


def ctime_cell_data_func(tree_column, cell, tree_model, iter, data):
    date = tree_model[iter][4]
    cell.set_property('text', date.strftime('%d %b %y'))


def size_cell_data_func(tree_column, cell, tree_model, iter, data):
    date = tree_model[iter][3]
    cell.set_property('text', psize(date))


class ListView(Gtk.TreeView):
    __gsignals__ = {
      'file-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
      # 'edit': (GObject.SIGNAL_RUN_FIRST, None, (object, object,)),
    }
    def __init__(self, accel=None):
        Gtk.TreeView.__init__(self, has_tooltip=True)
        # self.set_property('headers-visible', True)
        self.set_rules_hint(True)
        self.get_selection().set_mode(3)
        self.set_rubber_banding(True)
        self.set_search_column(2)
        self.set_enable_search(False)

        column = Gtk.TreeViewColumn(title='Set')
        column.set_resizable(True)
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','Ubuntu 10')
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 5)
        # column.set_sort_column_id(StoreMainPosition.SET)
        self.append_column(column)

        column = Gtk.TreeViewColumn('Mtime')
        column.set_clickable(True)
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        column.pack_start(renderer, True)

        column.set_cell_data_func(renderer, ctime_cell_data_func, func_data=None)
        # column.set_sort_column_id(4)        
        self.append_column(column)

        column = Gtk.TreeViewColumn('Size')
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        column.pack_start(renderer, True)
        # column.add_attribute(renderer, 'text', 8)
        column.set_cell_data_func(renderer, size_cell_data_func, func_data=None)        
        self.append_column(column)

        column = Gtk.TreeViewColumn('Count')
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        # renderer.set_property('alignment', 1)
        # column.set_cell_data_func(renderer, count_cell_data_func, func_data=None)
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 7)
        # column.set_sort_indicator(True)
        # column.set_clickable(True)
        self.append_column(column)

        column = Gtk.TreeViewColumn('Note')
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        renderer.set_property('ellipsize',3)
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 6)
        # column.set_sort_column_id(StoreMainPosition.NOTE)
        self.append_column(column)

        column = Gtk.TreeViewColumn('Filename')
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 2)
        # column.set_cell_data_func(renderer, file_cell_data_func, func_data=None)        
        # column.set_sort_column_id(1)
        self.append_column(column)

        menu = Gtk.Menu()
        read = Gtk.MenuItem.new_with_label('Open File')
        read.connect('activate', self.on_menu_read_activate)
        menu.append(read)
        update = Gtk.MenuItem.new_with_label('Update File')
        update.connect('activate', self.on_menu_edit_activated)
        menu.append(update)
        menu.show_all()

        self.connect('button-press-event', self.show_menu, menu)
        self.connect('row-activated', self.on_menu_read_activate)

    def show_menu(self, widget, event, menu):
        if event.button == Gdk.BUTTON_SECONDARY:
            menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        return None

    def on_menu_read_activate(self, widget, *args):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)
            fileview = self.get_parent().get_parent().get_parent()
            fileview.emit('file-update', model[iter][0])

    def on_menu_edit_activated(self, widget, *args):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        if paths:
            if not len(paths) >= 2:
                iter = model.get_iter(paths[0])
                fileview = self.get_parent().get_parent().get_parent()
                fileview.emit('file-update', model[iter][0])

    # def on_tooltip_queried(self, widget, x, y, keyboard_mode, tooltip):
    #     values = self.get_path_at_pos(x,y-24)
    #     if values:
    #         path, column, cell_x, cell_y = values
    #         if column.position == StoreMainPosition.THUMB:
    #             model = self.get_model()
    #             iter = model.get_iter(path)
    #             pix = model[iter][StoreMainPosition.THUMB]
    #             tooltip.set_icon(pix)
    #             return True


class IconView(Gtk.IconView):
    __gsignals__ = {
      'file-read': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
      'file-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
      # 'edit': (GObject.SIGNAL_RUN_FIRST, None, (object, object,)),
    }
    def __init__(self):
        Gtk.IconView.__init__(self, has_tooltip=True)
        self.set_item_width(0)
        self.set_property('margin',0)
        self.set_row_spacing(0)
        self.set_column_spacing(0)
        self.set_item_padding(1)

        # renderer = Gtk.CellRendererPixbuf()
        renderer = Gtk.CellRendererPixbuf()
        self.pack_start(renderer, False)
        renderer.set_alignment(0, 0)
        # self.thumb_renderer = renderer
        self.add_attribute(renderer,'pixbuf', 8)
        # self.add_attribute(renderer,'mime',StoreMainPosition.MIME)
       # self.set_cell_data_func(renderer,PixbufCellLayoutDataFunc,None)

        # srenderer = Gtk.CellRendererText()
        # self.pack_start(srenderer, False)
        # srenderer.set_property('font','Ubuntu 9')
        # srenderer.set_property('ellipsize', 2)
        # # srenderer.set_alignment(0.5, 0.5)
        # srenderer.set_property('max-width-chars', 10)
        # self.add_attribute(srenderer,'text', 5)
        
        # trenderer = Gtk.CellRendererText()
        # self.pack_start(trenderer, False)
        # self.add_attribute(trenderer,'text',StoreMainPosition.FILENAME)
        # # self.set_cell_data_func(trenderer,FileCellLayoutDataFunc,None)
        # trenderer.set_property('font','Ubuntu 9')
        # trenderer.set_alignment(0.5, 0.5)
        # trenderer.set_property('foreground','grey')
        # trenderer.set_property('ellipsize', 2)
        # trenderer.set_property('max-width-chars', 10)

        menu = Gtk.Menu()
        read = Gtk.MenuItem.new_with_label('Open File')
        read.connect('activate', self.on_menu_read_activate)
        menu.append(read)
        update = Gtk.MenuItem.new_with_label('Update File')
        update.connect('activate', self.on_menu_edit_activated)
        menu.append(update)
        menu.show_all()

        self.connect('button-press-event', self.show_menu, menu)
        self.connect('item-activated', self.on_menu_read_activate)

    def show_menu(self, widget, event, menu):
        if event.button == Gdk.BUTTON_SECONDARY:
            menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        return None

    def on_menu_read_activate(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)
        self.emit('file-read', model[iter][0])

    def on_menu_edit_activated(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if not len(paths) >= 2:
            iter = model.get_iter(paths[0])
            self.emit('file-update', model[iter][0])


class FileView(Gtk.Box):
    view = GObject.Property(type=str, default="listview")
    # tag_query = GObject.Property(type=int)

    __gsignals__ = {
        'file-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'tag-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    }
    '''
    Tagged File View
    '''

    def __init__(self, tag_id):
        Gtk.Box.__init__(self, orientation=1, spacing=0)


        search_bar = Gtk.SearchBar()
        searchentry = Gtk.SearchEntry()
        search_bar.add(searchentry)
        search_bar.connect_entry(searchentry)
        # search_bar.set_search_mode(True)
        self.pack_start(search_bar, False, True, 0)

        viewstore = ViewStore()
        # self.connect("notify::tag_query", self.on_tag_query_notified, viewstore)

        sub_stack = Gtk.Stack()
        scroll = Gtk.ScrolledWindow()
        scroll.set_property('shadow-type', 0)
        grid_view = IconView()
        grid_view.set_model(viewstore)
        # grid_view.connect('file-read', self.on_grid_file_read, stack)
        scroll.add(grid_view)
        sub_stack.add_named(scroll, 'gridview')
        # self.connect("notify::view", self.on_view_notified, sub_stack)

        scroll = Gtk.ScrolledWindow()
        scroll.set_property('shadow-type', 0)
        listview=ListView()
        listview.set_model(viewstore)
        # listview.connect('file-update', self.on_list_file_update, file_edit)
        scroll.add(listview)
        sub_stack.add_named(scroll, 'listview')
        self.stack = sub_stack


        self.pack_start(sub_stack, True, True, 0)
        self.show_all()
        sub_stack.set_visible_child_full('listview', 0)

        viewstore.set_query_tag_id(tag_id)

        # self.connect('file-update', self.a)

    # def on_tag_query_notified(self, object, gparamstring, model):
    #     print(self.tag_query)
    #     model.set_query_tag_id(self.tag_query)

    def on_tag_query_notified(self, object, gparamstring, stack):
        stack.set_visible_child_full(self.view, 0)

    def set_view(self, value):
        self.view = value
        self.stack.set_visible_child_full(value, 0)

