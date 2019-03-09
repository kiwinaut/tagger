from gi.repository import Gtk, GObject, GLib


class EditOverlay(Gtk.Overlay):
    __gsignals__ = {
        'updated': (GObject.SIGNAL_RUN_FIRST, None, (str, int,)),
    }
    def __init__(self):
        Gtk.Overlay.__init__(self)

        c = self.get_style_context()
        c.add_class('editpage')

        rev = Gtk.Revealer()
        rev.set_halign(3)
        rev.set_valign(2)
        box = Gtk.Box.new(orientation=0, spacing=4)
        context = box.get_style_context()
        context.add_class('app-notification')
        label = Gtk.Label('mmessage')
        box.pack_start(label, False, True, 0)
        rev.add(box)
        # rev.show_all()
        self.add_overlay(rev)
        self.connect('updated', self.on_show_message, label, context, rev)

    def on_show_message(self, widget, message, r, label, context, revealer):
        label.set_label(message)
        def close(*args):
            revealer.set_reveal_child(False)
            context.remove_class('app-notification-ok')
            context.remove_class('app-notification-error')
        if r > 0:
            context.add_class('app-notification-ok')
            revealer.set_reveal_child(True)
            GLib.timeout_add(2400, close, None)
        else:
            context.add_class('app-notification-error')
            revealer.set_reveal_child(True)
            GLib.timeout_add(4400, close, None)
