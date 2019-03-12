from gi.repository import Gtk
from config import CONFIG

class Notebook(Gtk.Notebook):
    def __init__(self):
        Gtk.Notebook.__init__(self)

    def append_buttom(self, child, label, icon_label="default"):
        img = Gtk.Image.new_from_file(f'{CONFIG["static"]}/{icon_label}.png')
        closebutton = Gtk.Button.new_from_icon_name('window-close-symbolic', 2)
        # closebutton.set_css_name('small-button')
        closebutton.set_relief(2)
        closebutton.connect('clicked', self.on_tab_close, child)
        label = Gtk.Label(label)
        label.set_ellipsize(3)
        label.set_size_request(100, -1)
        box = Gtk.Box.new(orientation=0, spacing=0)
        box.pack_start(img, False, False, 0)
        box.pack_start(label, True, True, 0)
        box.pack_start(closebutton, False, False, 0)
        box.show_all()

        return self.append_page(child, box)

    def append_static(self, child, label):
        label = Gtk.Label(label)
        label.set_ellipsize(3)
        label.set_size_request(100, -1)
        box = Gtk.Box.new(orientation=0, spacing=0)
        box.pack_start(label, True, True, 0)
        box.show_all()

        return self.append_page(child, box)

    def on_tab_close(self, widget, child):
        num = self.page_num(child)
        self.remove_page(num)


# system-search-symbolic  filelist
# folder-documents-symbolic   fileedit
# avatar-default-symbolic     tag
# content-loading-symbolic  all
# document-edit-symbolic