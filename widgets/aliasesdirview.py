from gi.repository import Gtk, Gdk, GObject
from widgets.widgets import TagTreeView, target3, target4
from data_models import col_store
from models import Query
from stores import TagStore
from data_models import TabModel
from decorators import wait


clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)


class IconTagView(Gtk.IconView):
    def __init__(self):
        Gtk.IconView.__init__(self, has_tooltip=True)

        self.set_item_width(0)
        self.set_row_spacing(0)
        self.set_column_spacing(0)

        renderer = Gtk.CellRendererPixbuf()
        self.pack_start(renderer, False)
        # renderer.set_alignment(0, 0)
        self.add_attribute(renderer,'pixbuf', 4)

        srenderer = Gtk.CellRendererText()
        srenderer.set_property('width', 118)
        srenderer.set_property('xalign', .5)

        self.pack_start(srenderer, False)
        # srenderer.set_property('font','Ubuntu 9')
        srenderer.set_property('ellipsize', 2)
        # srenderer.set_property('max-width-chars', 10)
        self.add_attribute(srenderer,'text', 1)

        srenderer = Gtk.CellRendererText()
        srenderer.set_property('xalign', .5)
        self.pack_start(srenderer, False)
        self.add_attribute(srenderer,'text', 5)

        menu = Gtk.Menu()
        delete = Gtk.MenuItem.new_with_label('File List')
        delete.connect('activate', self.on_menu_read_activate)
        menu.append(delete)
        delete = Gtk.MenuItem.new_with_label('Tag Edit')
        delete.connect('activate', self.on_menu_update_activate)
        menu.append(delete)
        delete = Gtk.MenuItem.new_with_label('Copy Name')
        delete.connect('activate', self.on_menu_copy_name_activate)
        menu.append(delete)
        delete = Gtk.MenuItem.new_with_label('Open First')
        delete.connect('activate', self.on_menu_open_first_activate)
        menu.append(delete)
        menu.show_all()
        self.menu = menu
        # self.connect('button-press-event', self.show_menu, menu)
        self.connect('item-activated', self.on_menu_read_activate)

        self.enable_model_drag_source(
            Gdk.ModifierType.BUTTON1_MASK|Gdk.ModifierType.CONTROL_MASK,
            [target4],
            Gdk.DragAction.COPY
        )
        self.connect("drag-data-get", self.on_drag_data_get)

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        paths = self.get_selected_items()
        model = self.get_model()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)

            if str(data.get_target()) == 'TAG':
                value = str(model[iter][0])
                print(value)
                data.set(data.get_target(), 8, bytes(value, "utf-8"))
        # elif str(data.get_target()) == 'text/plain':
        #     string = model[iter][1]
        #     data.set(data.get_target(), 8, bytes(string, "utf-8"))


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
        elif event.button == Gdk.BUTTON_MIDDLE:
            path = self.get_path_at_pos(event.x, event.y)
            self.select_path(path)
            model = self.get_model()
            iter = model.get_iter(path)
            parent = self.get_parent().get_parent().get_parent()
            parent.emit('tag-edit', model[iter][0], model[iter][1])
        else:
            Gtk.IconView.do_button_press_event(self, event)

    def on_menu_open_first_activate(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)
            clipboard.set_text(model[iter][1], -1)

    def on_menu_copy_name_activate(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)
            clipboard.set_text(model[iter][1], -1)

    def on_menu_read_activate(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)
            parent = self.get_parent().get_parent().get_parent()
            parent.emit('file-list', model[iter][0], model[iter][1])

    def on_menu_update_activate(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)
            parent = self.get_parent().get_parent().get_parent()
            parent.emit('tag-edit', model[iter][0], model[iter][1])


class TagViewTest(Gtk.TreeView):
    # __gsignals__ = {
    #     'tag-read': (GObject.SIGNAL_RUN_FIRST, None, ()),
    #     'tag-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
    #     'tag-delete': (GObject.SIGNAL_RUN_FIRST, None, ()),
    #     'filenames': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    # }
    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.set_enable_search(False)
        self.set_property('headers-visible', False)

        column = Gtk.TreeViewColumn('name')


        pb = Gtk.CellRendererPixbuf()
        column.pack_start(pb, False)
        column.add_attribute(pb, 'pixbuf', 4)

        alias = Gtk.CellRendererText()
        column.pack_start(alias, True)
        column.add_attribute(alias, 'text', 1)

        # renderer = Gtk.CellRendererText()
        # column.pack_start(renderer, False)
        # column.add_attribute(renderer, 'text', 2)
        self.append_column(column)

        menu = Gtk.Menu()
        # delete = Gtk.MenuItem.new_with_label('Delete')
        # delete.connect('activate', self.on_menu_delete_activate)
        # menu.append(delete)
        delete = Gtk.MenuItem.new_with_label('File List')
        delete.connect('activate', self.on_menu_read_activate)
        menu.append(delete)
        delete = Gtk.MenuItem.new_with_label('Tag Edit')
        delete.connect('activate', self.on_menu_update_activate)
        menu.append(delete)
        # delete = Gtk.MenuItem.new_with_label('Filenames')
        # delete.connect('activate', self.on_menu_filenames_activate)
        # menu.append(delete)

        menu.show_all()
        self.connect('button-press-event', self.show_menu, menu)

        # self.enable_model_drag_source(
        #     Gdk.ModifierType.BUTTON1_MASK|Gdk.ModifierType.CONTROL_MASK,
        #     [target3, target4],
        #     Gdk.DragAction.COPY
        # )
        # self.connect("drag-data-get", self.on_drag_data_get)


    def on_drag_data_get(self, widget, drag_context, data, info, time):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        # path = model.get_path(iter)
        # value = '{}\n{}'.format(*model.get(iter, 0, 1))
        # value = path.to_string()
        if str(data.get_target()) == 'TAG':
            value = str(model[iter][0])
            data.set(data.get_target(), 8, bytes(value, "utf-8"))
        elif str(data.get_target()) == 'text/plain':
            string = model[iter][1]
            data.set(data.get_target(), 8, bytes(string, "utf-8"))


    def on_menu_filenames_activate(self, widget, *args):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        # self.emit('tag-read', model[iter][0], model[iter][1])
        self.emit('filenames', model[iter][0])

    def on_menu_read_activate(self, widget, *args):
        # selection = self.get_selection()
        # model, iter = selection.get_selected()
        # self.emit('tag-read', model[iter][0], model[iter][1])
        parent = widget.get_parent()
        parent.emit('tag-read')

    def on_menu_update_activate(self, widget, *args):
        # selection = self.get_selection()
        # model, iter = selection.get_selected()
        # self.emit('tag-update', model[iter][0], model[iter][1])

        self.emit('tag-update')#tag_id
        # somewhere updated
        # update model in here or there?

    def on_menu_delete_activate(self, widget, *args):
        # sure
        # db del
        # self del

        # selection = self.get_selection()
        # model, iter = selection.get_selected()
        # self.emit('tag-delete', model[iter][0], model[iter][1])
        self.emit('tag-delete')

    def show_menu(self, widget, event, menu):
        if event.button == Gdk.BUTTON_SECONDARY:
            menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        return None

class AliasesDirView(Gtk.Box):

    __gsignals__ = {
        'file-list': (GObject.SIGNAL_RUN_FIRST, None, (int, str,)),
        'tag-edit': (GObject.SIGNAL_RUN_FIRST, None, (int, str,)),
    }
    def __init__(self):
        Gtk.Box.__init__(self, orientation=0, spacing=0)
        self.set_name('dirview')
        fbox = Gtk.Box.new(orientation=1, spacing=0)
        self.tab_model = TabModel()
        self.tab_model.name = 'search'

        tag_store = TagStore()
        self.tab_model.connect("notify::scalefactor", self.on_scalefactor_notified, tag_store)

        #TAG VIEW
        tag_scroll = Gtk.ScrolledWindow()
        # tag_scroll.set_property('shadow-type', 1)
        # tag_store = TagStore()
        # col_model.connect('col-changed', self.on_model_col_changed)
        # col_model.connect('folder-changed', self.on_model_col_changed)
        tag_view = IconTagView()
        tag_view.set_model(tag_store)
        # tag_view.connect('tag-read', self.on_tag_read)
        # tag_view.connect('row-activated', self.on_tag_read)
        # tag_view.connect('tag-update', self.on_tag_edit)
        # tag_view.connect('filenames', self.on_tag_filenames, clipboard)
        tag_scroll.add(tag_view)
        fbox.pack_start(tag_scroll, True, True, 0)
        self.pack_end(fbox, True, True, 0)

        #COLLECTION VIEW
        fbox = Gtk.Box.new(orientation=1, spacing=0)
        fbox.set_property('margin',3)

        alias_entry = Gtk.SearchEntry()
        alias_entry.connect('search-changed', self.on_tag_filter_changed, tag_store)
        alias_entry.set_valign(3)
        fbox.pack_start(alias_entry, False, True, 0)
        
        col_scroll = Gtk.ScrolledWindow()
        # col_scroll.set_property('margin-left',3)
        # col_scroll.set_property('margin-right',3)
        # col_scroll.set_property('shadow-type', 1)
        tree_view = TagTreeView()
        tree_view.connect('tag-read', self.on_col_read_activated)
        tree_view.connect('row-activated', self.on_col_read_activated, tag_store)

        # col_store = ColStore()
        tree_view.set_model(col_store)
        tree_view.expand_all()
        col_scroll.add(tree_view)
        col_scroll.set_size_request(240, -1)

        fbox.pack_start(col_scroll, True, True, 0)
        self.pack_end(fbox, False, True, 0)

        self.show_all()

    def on_scalefactor_notified(self, obj, gparam, store):
        store.set_scale(self.tab_model.scalefactor)

    def on_tag_filter_changed(self, widget, store):
        text = widget.get_text()
        store.set_query_like_text(text)

    @wait
    def on_col_read_activated(self, widget, path, column, store, callback):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        store.set_query_from_folder(model[iter][0], callback)

