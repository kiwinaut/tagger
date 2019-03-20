from gi.repository import Gtk, GObject, Gdk, GLib, Gio
from gi.repository.GdkPixbuf import Pixbuf
from data_models import TabModel
import pathlib
import threading
from decorators import wait


class InstaStore(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(
            self,
            str,     # 0 filepath
            Pixbuf,  #1 thumb
        )
        self.undo = None

    def set_folderpath(self, path, finish_cb):
        self.clear()
        p = pathlib.Path(path)
        # print(p.glob('*.jpg'))
        for p in p.glob('*.jpg'):
            self.append((str(p), None))

        # print(len(self))

        def add_pb(model, path, iter, data):
            try:
                pb = Pixbuf.new_from_file_at_size(model[iter][0], 256, 256)
            except GLib.Error:
                pb = None
            GLib.idle_add(self.set_value, iter, 1, pb)

        def another():
            self.foreach(add_pb, None)
            finish_cb()

        thread = threading.Thread(target=another, daemon=True)
        # thread = threading.Thread(target=self.foreach, args=[add_pb, None], daemon=True)
        thread.start()


class InstaView(Gtk.IconView):
    def __init__(self):
        Gtk.IconView.__init__(self)

        self.set_item_width(0)
        self.set_row_spacing(0)
        self.set_column_spacing(0)

        renderer = Gtk.CellRendererPixbuf()
        self.pack_start(renderer, False)
        # renderer.set_alignment(0, 0)
        self.add_attribute(renderer,'pixbuf', 1)

        # srenderer = Gtk.CellRendererText()
        # srenderer.set_property('width', 118)
        # srenderer.set_property('xalign', .5)

        # self.pack_start(srenderer, False)
        # # srenderer.set_property('font','Ubuntu 9')
        # srenderer.set_property('ellipsize', 2)
        # # srenderer.set_property('max-width-chars', 10)
        # self.add_attribute(srenderer,'text', 1)


        menu = Gtk.Menu()        
        delete = Gtk.MenuItem.new_with_label('Undo')
        # delete.connect('activate', self.on_menu_read_activate)
        menu.append(delete)
        # delete = Gtk.MenuItem.new_with_label('Tag Edit')
        # delete.connect('activate', self.on_menu_update_activate)
        # menu.append(delete)
        # delete = Gtk.MenuItem.new_with_label('Copy Name')
        # delete.connect('activate', self.on_menu_copy_name_activate)
        # menu.append(delete)
        # delete = Gtk.MenuItem.new_with_label('Open First')
        # delete.connect('activate', self.on_menu_open_first_activate)
        # menu.append(delete)
        # menu.show_all()
        # self.menu = menu
        self.connect('button-release-event', self.show_menu, menu)
        self.connect('item-activated', self.on_open_image)
        self.set_activate_on_single_click(True)

    def show_menu(self, widget, event, menu):
        path = self.get_path_at_pos(event.x, event.y)
        self.select_path(path)
        model = self.get_model()

        if event.button == Gdk.BUTTON_MIDDLE:
            iter = model.get_iter(path)
            f = Gio.File.new_for_path(model[iter][0])
            if f.trash(None):
                model.remove(iter)
        elif event.button == Gdk.BUTTON_SECONDARY:
            menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        return None

    def on_open_image(self, widget, path):
        # paths = self.get_selected_items()
        model = self.get_model()
        # if paths:
        #     path = paths[0]
        iter = model.get_iter(path)
        img = Gtk.Image.new_from_file(model[iter][0])
        # pb = img.get_pixbuf()
        # if pb.get_height() > 1080 
        pop = Gtk.Window.new(1)
        # scroll = Gtk.ScrolledWindow()
        # scroll.set_pre
        # scroll.add(img)
        pop.add(img)
        pop.set_position(3)
        pop.show_all()
        pop.connect('button-release-event', self.on_pop_click)


        #open
    def on_pop_click(self, widget, path):
        widget.close()

class InstaBox(Gtk.Box):
    # folderpath = GObject.Property(type=str, default="")

    # __gsignals__ = {
    #     'file-list': (GObject.SIGNAL_RUN_FIRST, None, (int, str,)),
    #     'tag-edit': (GObject.SIGNAL_RUN_FIRST, None, (int, str,)),
    # }
    def __init__(self):
        Gtk.Box.__init__(self, orientation=1, spacing=0)
        fbox = Gtk.Box.new(orientation=0, spacing=5)
        fbox.set_property('margin', 5)
        filebut = Gtk.FileChooserButton.new('Open Folder',2)
        filebut.add_shortcut_folder('/home/soni/Downloads/p/instagram')
        fbox.pack_start(filebut, False, False, 0)

        but = Gtk.Button('Undo')
        fbox.pack_start(but, False, False, 0)

        but = Gtk.Button('Reload')
        fbox.pack_start(but, False, False, 0)

        but = Gtk.Button('Zip')
        fbox.pack_start(but, False, False, 0)





        self.tab_model = TabModel()
        self.tab_model.name = 'insta'

        insta_store = InstaStore()
        filebut.connect('file-set', self.on_folder_set, insta_store)

        #TAG VIEW
        tag_scroll = Gtk.ScrolledWindow()
        # tag_scroll.set_property('shadow-type', 1)
        # tag_store = TagStore()
        # col_model.connect('col-changed', self.on_model_col_changed)
        # col_model.connect('folder-changed', self.on_model_col_changed)
        tag_view = InstaView()
        tag_view.set_model(insta_store)
        # tag_view.connect('tag-read', self.on_tag_read)
        # tag_view.connect('row-activated', self.on_tag_read)
        # tag_view.connect('tag-update', self.on_tag_edit)
        # tag_view.connect('filenames', self.on_tag_filenames, clipboard)
        tag_scroll.add(tag_view)
        self.pack_start(fbox, False, True, 0)
        self.pack_start(tag_scroll, True, True, 0)

    @wait
    def on_folder_set(self, button, store, callback):
        f = button.get_file()
        store.set_folderpath(f.get_path(), callback)
