from gi.repository import Gtk, GObject
from stores import missing
from gi.repository.GdkPixbuf import Pixbuf

class TagFlowBox(Gtk.FlowBox):
    __gsignals__ = {
        "child-deleted": (GObject.SignalFlags.RUN_FIRST, None, (GObject.GObject,)),
        "child-clicked": (GObject.SignalFlags.RUN_FIRST, None, (GObject.GObject,))
    }
    def __init__(self):
        Gtk.FlowBox.__init__(self)
        self.set_selection_mode(0)
        self.set_row_spacing(0)
        self.set_column_spacing(0)
        self.set_orientation(0)
        self.set_activate_on_single_click(True)
        # c = self.get_style_context()
        # c.add_class('aliases')
        # self.connect('child-activated', self.on_child_activated)

    def add_tagchild(self, id, label):
        child = Gtk.FlowBoxChild()
        child.id = id
        child.label = label
        # child.set_halign(1)
        # child.set_valign(1)

        box = Gtk.Box.new(orientation=0, spacing=0)
        c = box.get_style_context()
        c.add_class('alias')

        link_event = Gtk.EventBox()
        labelw = Gtk.Label(label.title())
        link_event.add(labelw)
        link_event.connect('button-release-event', self.on_link_clicked, child)
        box.pack_start(link_event, True, True, 0)

        del_but = Gtk.Button.new_from_icon_name('window-close-symbolic', 2)
        del_but.connect('clicked', self.on_del_clicked, child)
        del_but.set_relief(2)
        del_but.set_can_focus(False)
        del_but.set_halign(3)
        del_but.set_valign(3)
        c = del_but.get_style_context()
        c.add_class('delbut')
        box.pack_start(del_but, False, False, 0)

        child.add(box)
        child.show_all()

        self.add(child)

    def add_sggstchild(self, row):
        child = Gtk.FlowBoxChild()
        child.id = row[0]
        child.label = row[1]
        try:
            pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{row[2]}.jpg', 256, 256)
        except:
            pb = missing
        child.thumb = pb

        child.set_has_tooltip(True)
        child.connect('query-tooltip', self.on_label_tooltip_queried)
        # child.set_halign(1)
        # child.set_valign(1)

        box = Gtk.Box.new(orientation=0, spacing=0)
        c = box.get_style_context()
        c.add_class('sggst')

        link_event = Gtk.EventBox()
        labelw = Gtk.Label(child.label.title())
        link_event.add(labelw)
        link_event.connect('button-release-event', self.on_link_clicked, child)
        box.pack_start(link_event, True, True, 0)

        child.add(box)
        child.show_all()

        self.add(child)

    def on_link_clicked(self, widget, event, child):
        self.emit('child-clicked', child)

    def on_del_clicked(self, widget, child):
        self.emit('child-deleted', child)

    def on_label_tooltip_queried(self, widget, x, y, keyboard_mode, tooltip):
        tooltip.set_icon(widget.thumb)
        return True

    # def on_child_activated(self, flow_box, child):
    #     # label = child.get_child().id
    #     print(child.id)
