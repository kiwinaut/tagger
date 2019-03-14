from gi.repository import Gtk, GObject, Gdk
from print_pretty.pretty_size import psize
from stores import ViewStore, AllViewStore
from data_models import TabModel
# from widgets import MainSignals
from shell_commands import open_file
from models import Query

def ctime_cell_data_func(tree_column, cell, tree_model, iter, data):
    date = tree_model[iter][4]
    cell.set_property('text', date.strftime('%d %b %y'))


def size_cell_data_func(tree_column, cell, tree_model, iter, data):
    date = tree_model[iter][3]
    cell.set_property('text', psize(date))


class ListView(Gtk.TreeView):
    # __gsignals__ = {
    #   'file-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    #   # 'edit': (GObject.SIGNAL_RUN_FIRST, None, (object, object,)),
    # }
    def __init__(self, header=True):
        Gtk.TreeView.__init__(self)
        self.set_property('headers-visible', header)
        self.set_rules_hint(True)
        self.get_selection().set_mode(3)
        self.set_rubber_banding(True)
        self.set_search_column(2)
        self.set_enable_search(False)

        column = Gtk.TreeViewColumn(title='Set')
        column.set_resizable(True)
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 5)
        column.set_sort_column_id(5)
        self.append_column(column)

        column = Gtk.TreeViewColumn('Mtime')
        column.set_clickable(True)
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)

        column.set_cell_data_func(renderer, ctime_cell_data_func, func_data=None)
        # column.set_sort_column_id(4)        
        self.append_column(column)

        column = Gtk.TreeViewColumn('Size')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        # column.add_attribute(renderer, 'text', 8)
        column.set_sort_column_id(3)
        column.set_cell_data_func(renderer, size_cell_data_func, func_data=None)        
        self.append_column(column)

        column = Gtk.TreeViewColumn('Count')
        renderer = Gtk.CellRendererText()
        # column.set_cell_data_func(renderer, count_cell_data_func, func_data=None)
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 7)
        column.set_sort_column_id(7)
        self.append_column(column)

        column = Gtk.TreeViewColumn('Note')
        renderer = Gtk.CellRendererText()
        renderer.set_property('ellipsize',3)
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 6)
        column.set_sort_column_id(6)
        self.append_column(column)

        column = Gtk.TreeViewColumn('Filename')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.set_sort_column_id(2)
        column.add_attribute(renderer, 'text', 2)
        # column.set_cell_data_func(renderer, file_cell_data_func, func_data=None)        
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
            # scrolled = row.get_ancestor(Gtk.ScrolledWindow)
            fileview.emit('file-edit', model[iter][0], model[iter][2])

    def on_menu_edit_activated(self, widget, *args):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        if paths:
            if not len(paths) >= 2:
                iter = model.get_iter(paths[0])
                fileview = self.get_parent().get_parent().get_parent()
                fileview.emit('file-edit', model[iter][0])

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
    # __gsignals__ = {
    #   'file-read': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    #   'file-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    #   # 'edit': (GObject.SIGNAL_RUN_FIRST, None, (object, object,)),
    # }
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
        self.menu = menu
        menu.show_all()

        self.connect('item-activated', self.on_menu_edit_activated)



    def on_menu_read_activate(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)
            parent = self.get_parent().get_parent().get_parent()
            # parent.emit('tag-edit', model[iter][0], model[iter][1])

    def on_menu_edit_activated(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if not len(paths) >= 2:
            iter = model.get_iter(paths[0])
            parent = self.get_parent().get_parent().get_parent()
            parent.emit('file-edit', model[iter][0], model[iter][2])

    def do_button_press_event(self, event):
        if event.button == Gdk.BUTTON_SECONDARY:
            selection = self.get_selected_items()
            path = self.get_path_at_pos(event.x, event.y)
            # selection = self.get_selection()
            # pos = self.get_path_at_pos(event.x, event.y)# path, column, cell_x, cell_y
            if path:
                #clicked any content
                if path in selection:
                    #clicked in selection
                    self.menu.popup(None, None, None, None, event.button, event.time)
                else:
                    #clicked outside of selection
                    # Gtk.IconView.do_button_press_event(self, event)
                    self.unselect_all()
                    self.select_path(path)

                    self.menu.popup(None, None, None, None, event.button, event.time)
            else:
                #clicked empty area
                self.unselect_all()
                return False
        elif event.button == Gdk.BUTTON_MIDDLE:
            path = self.get_path_at_pos(event.x, event.y)
            self.select_path(path)
            model = self.get_model()
            iter = model.get_iter(path)
            filepath = Query.get_file_path(model[iter][0])
            open_file(filepath, 'mcomix')
        else:
            Gtk.IconView.do_button_press_event(self, event)

class FileView(Gtk.Box):
    view = GObject.Property(type=str, default="listview")
    # tag_query = GObject.Property(type=int)

    __gsignals__ = {
        'file-edit': (GObject.SIGNAL_RUN_FIRST, None, (int,str,)),
        'tag-edit': (GObject.SIGNAL_RUN_FIRST, None, (int,str,)),
    }
    '''
    Tagged File View
    '''

    def __init__(self, tag_id, alias_name):
        Gtk.Box.__init__(self, orientation=1, spacing=0)
        self.alias = alias_name
        self.tab_model = TabModel()
        self.tab_model.name = 'stack'
        search_bar = Gtk.SearchBar()
        searchentry = Gtk.SearchEntry()
        search_bar.add(searchentry)
        search_bar.set_show_close_button(True)
        search_bar.connect_entry(searchentry)
        # search_bar.set_search_mode(True)
        self.pack_start(search_bar, False, True, 0)
        self.connect('key-press-event', self.on_sstack_key_pressed, search_bar)

        viewstore = ViewStore()
        self.tab_model.connect("notify::scalefactor", self.on_scalefactor_notified, viewstore)
        searchentry.connect('search-changed', self.on_file_filter_changed, viewstore)
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

    def on_scalefactor_notified(self, obj, gparam, store):
        store.set_scale(self.tab_model.scalefactor)

    def on_tag_query_notified(self, object, gparamstring, stack):
        stack.set_visible_child_full(self.view, 0)

    def set_view(self, value):
        self.view = value
        self.stack.set_visible_child_full(value, 0)

    def on_sstack_key_pressed(self, widget, event, search_bar):
        search_bar.handle_event(event)

    def on_file_filter_changed(self, widget, store):
        text = widget.get_text()
        store.set_query_filter_text(text)


class AllFileView(Gtk.Box):
    view = GObject.Property(type=str, default="listview")
    # query_fn_filter = GObject.Property(type=str, default="")
    # query_page = GObject.Property(type=int, default=1)
    # query_sort = GObject.Property(type=str, default="mtime")
    # query_order = GObject.Property(type=str, default="desc")
    # query_media = GObject.Property(type=str, default="archives")
    # scalefactor = GObject.Property(type=float, default=6.0)
    # tag_query = GObject.Property(type=int)

    __gsignals__ = {
        'file-edit': (GObject.SIGNAL_RUN_FIRST, None, (int,str,)),
        'tag-edit': (GObject.SIGNAL_RUN_FIRST, None, (int,str,)),
    }
    '''
    Tagged File View
    '''

    def __init__(self, all_file_code=0):
        Gtk.Box.__init__(self, orientation=1, spacing=0)
        if all_file_code == 0:
            self.alias = 'All Files'
        elif all_file_code == 1:
            self.alias = '1 Tagged Files'
        elif all_file_code == -1:
            self.alias = 'Untagged Files'

        self.tab_model = TabModel()
        self.tab_model.name = 'stack'
        viewstore = AllViewStore()
        self.tab_model.connect("notify::scalefactor", self.on_scalefactor_notified, viewstore)
        #REVEALER
        rev = Gtk.Revealer()
        box = Gtk.Box.new(orientation=0, spacing=5)
        box.set_property('margin', 5)

        entry = Gtk.SearchEntry()
        entry.set_placeholder_text('Filename like')
        entry.connect('search-changed', self.on_filter_search_changed, viewstore)
        box.pack_start(entry, True, True, 0)

        spin_button = Gtk.SpinButton.new_with_range(1,9999,1)
        # entry.set_size_request(20,12)
        spin_button.set_property('width-request', 20)
        spin_button.connect('value-changed', self.on_page_changed, viewstore)
        box.pack_start(spin_button, False, False, 0)

        sortcombo = Gtk.ComboBoxText()
        sortcombo.append_text('Filename')
        sortcombo.append_text('Set')
        sortcombo.append_text('Mtime')
        sortcombo.append_text('Count')
        sortcombo.append_text('Size')
        sortcombo.set_active(0)
        sortcombo.connect('changed', self.on_sort_combo_changed, viewstore)
        box.pack_start(sortcombo, False, True, 0)

        ordercombo = Gtk.ComboBoxText()
        ordercombo.append_text('Desc')
        ordercombo.append_text('Asc')
        ordercombo.set_active(0)
        ordercombo.connect('changed', self.on_order_combo_changed, viewstore)
        box.pack_start(ordercombo, False, True, 0)

        closebutton = Gtk.Button.new_from_icon_name('window-close-symbolic', 2)
        closebutton.connect('clicked', self.on_revealer_close, rev)
        box.pack_start(closebutton, False, True, 0)

        self.connect('key-press-event', self.on_key_pressed, rev)
        rev.add(box)

        self.pack_start(rev, False, True, 0)
        #
        # self.connect('key-press-event', self.on_sstack_key_pressed, search_bar)

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
        listview=ListView(header=False)
        listview.set_model(viewstore)
        # listview.connect('file-update', self.on_list_file_update, file_edit)
        scroll.add(listview)
        sub_stack.add_named(scroll, 'listview')
        self.stack = sub_stack


        self.pack_start(sub_stack, True, True, 0)
        self.show_all()
        sub_stack.set_visible_child_full('listview', 0)
        viewstore.set_code(all_file_code)

    def on_scalefactor_notified(self, obj, gparam, store):
        store.set_scale(self.tab_model.scalefactor)


    def on_page_changed(self, widget, store):
        store.set_page(widget.get_value())

    def on_order_combo_changed(self, widget, store):
        store.set_order(widget.get_active_text())

    def on_sort_combo_changed(self, widget, store):
        store.set_sort(widget.get_active_text())

    def on_filter_search_changed(self, widget, store):
        store.set_fn_filter(widget.get_text())

    def on_tag_query_notified(self, object, gparamstring, stack):
        stack.set_visible_child_full(self.view, 0)

    def set_view(self, value):
        self.view = value
        self.stack.set_visible_child_full(value, 0)

    def on_key_pressed(self, widget, event, rev):
        rev.set_reveal_child(True)

    def on_revealer_close(self, widget, rev):
        rev.set_reveal_child(False)

    def on_file_filter_changed(self, widget, store):
        text = widget.get_text()
        store.set_query_filter_text(text)
