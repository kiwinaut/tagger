from gi.repository import Gtk

class Notebook(Gtk.Notebook):
    def __init__(self):
        Gtk.Notebook.__init__(self)

    def append_buttom(self, child, label):
        closebutton = Gtk.Button.new_from_icon_name('window-close-symbolic', 2)
        # closebutton.set_css_name('small-button')
        closebutton.set_relief(2)
        closebutton.connect('clicked', self.on_tab_close, child)
        label = Gtk.Label(label)
        box = Gtk.Box.new(orientation=0, spacing=0)
        box.pack_start(label, True, True, 0)
        box.pack_start(closebutton, False, True, 0)
        box.show_all()

        return self.append_page(child, box)

    def on_tab_close(self, widget, child):
        num = self.page_num(child)
        self.remove_page(num)