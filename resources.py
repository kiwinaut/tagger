from gi.repository import GdkPixbuf, Gtk, GObject

icon_theme = Gtk.IconTheme.get_default()

queued_pixbuf = icon_theme.load_icon('appointment-soon', 16, Gtk.IconLookupFlags.USE_BUILTIN)
active_pixbuf = icon_theme.load_icon('media-playback-start', 16, Gtk.IconLookupFlags.USE_BUILTIN)
download_pixbuf = icon_theme.load_icon('emblem-downloads', 16, Gtk.IconLookupFlags.USE_BUILTIN)
solving = icon_theme.load_icon('document-open-recent', 16, Gtk.IconLookupFlags.USE_BUILTIN)
error = icon_theme.load_icon('emblem-important', 16, Gtk.IconLookupFlags.USE_BUILTIN)

# queued_pixbuf = GdkPixbuf.Pixbuf.new_from_file('appointment-soon', 2)
# active_pixbuf = GdkPixbuf.Pixbuf.new_from_file('media-playback-start', 2)
# download_pixbuf = GdkPixbuf.Pixbuf.new_from_file('emblem-downloads', 2)
# solving = GdkPixbuf.Pixbuf.new_from_file('emblem-downloads', 2)
# tag_pixbuf = GdkPixbuf.Pixbuf.new_from_file('resources/pix/emblem-generic.png')
# search_pixbuf = GdkPixbuf.Pixbuf.new_from_file('/usr/share/icons/Adwaita/16x16/places/folder-saved-search.png')

set_model = Gtk.ListStore(int, object, int, str, str, str)
downmodel = Gtk.ListStore(int, object, int, GObject.TYPE_UINT64, str, str)
# id, status, percentage, size, set,host

