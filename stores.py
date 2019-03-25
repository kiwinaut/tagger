from gi.repository import Gtk, GObject, GLib
from gi.repository.GdkPixbuf import Pixbuf
from models import Query
# from decorators import wait
import threading
# import multiprocessing
from gi.repository.Gio import File
from config import CONFIG

IMGPATH = CONFIG['indexer.thumb_location']


theme = Gtk.IconTheme.get_default()
missing = theme.load_icon('image-missing',64, Gtk.IconLookupFlags.USE_BUILTIN)
avatar = theme.load_icon('avatar-default-symbolic',64, Gtk.IconLookupFlags.USE_BUILTIN)

# avatar = Pixbuf.new_from_file_at_size('/usr/share/icons/Adwaita/256x256/status/avatar-default.png', 32, 32)

class TagStore(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(
            self,
            int,     # 0 id
            str,     # 1 
            str,     # 2 
            str,     # 3 
            Pixbuf,  #4 thumb
            str     # 5
        )
        self.load_busy = False
        self.text_buf = []

    def set_query_from_folder(self, fol_int, finish_cb):
        self.clear()
        for q in Query.get_tags(fol_int):
            self.append((*q[:4], None, q[4], ))

        def add_pb(model, path, iter, data):
            try:
                pb = Pixbuf.new_from_file_at_size(IMGPATH.format(model[iter][3]), 192, 192)
            except GLib.Error:
                pb = avatar
            GLib.idle_add(self.set_value, iter, 4, pb)

        def another(finish_cb):
            self.foreach(add_pb, None)
            finish_cb()

        # thread = multiprocessing.Process(target=another, args=(finish_cb,), daemon=True)
        # thread.start()
        thread = threading.Thread(target=another, name='tag', args=(finish_cb,), daemon=True)
        thread.start()

    def set_query_from_folder2(self, fol_int):
        self.clear()
        for q in Query.get_tags(folder_id=fol_int):
            try:
                pb = Pixbuf.new_from_file_at_size(IMGPATH.format(q[3]), 192, 192)
            except GLib.Error:
                pb = avatar
            self.append((*q[:4], pb, q[4], ))

    def set_query_like_text(self, text):
        self.clear()
        if text == "":
            return
        for q in Query.get_tags(filter_text=text):
            try:
                pb = Pixbuf.new_from_file_at_size(IMGPATH.format(q[3]), 192, 192)
            except GLib.Error:
                pb = avatar
            self.append((*q[:4], pb,q[4],))

    def set_scale(self, value):
        size = 32 * value
        avatar = theme.load_icon('avatar-default-symbolic',size, Gtk.IconLookupFlags.USE_BUILTIN)
        def add_pb(model, path, iter, data):
            try:
                pb = Pixbuf.new_from_file_at_size(IMGPATH.format(model[iter][3]), size, size)
            except GLib.Error:
                pb = avatar
            model.set_value(iter, 4, pb)
        self.foreach(add_pb, None)


class ViewStore(Gtk.ListStore):
    def __init__(self, scale=4.0):
        Gtk.ListStore.__init__(
            self,
            int,     # 0 file_id
            str,     # 1 filepath
            str,     # 2 filename
            GObject.TYPE_UINT64, #3 size
            object,  #4 mtime
            str,     #5 set
            str,     #6 note 
            int,     #7 count
            # int,     #8 duration
            Pixbuf,  #9 thumb
        )
        self.scale = scale * 32
        self.missing = theme.load_icon('image-missing', self.scale, Gtk.IconLookupFlags.USE_BUILTIN)


    def set_scale(self, value):
        self.scale = 32 * value
        self.missing = theme.load_icon('image-missing', self.scale, Gtk.IconLookupFlags.USE_BUILTIN)
        scale = self.scale
        missing = self.missing
        def add_pb(model, path, iter, data):
            try:
                pb = Pixbuf.new_from_file_at_size(IMGPATH.format(model[iter][0]), scale, scale)
            except GLib.Error:
                pb = missing
            model.set_value(iter, 8, pb)
        self.foreach(add_pb, None)

    def append_from_query(self, query):
        for q in query:
            self.append(q)

    def set_query_tag_id(self, tag_id):
        scale = self.scale
        missing = self.missing
        self.tag_id = tag_id
        sq = Query.get_files('archives', 'filepath', 'desc', tag_id)
        # sq = Query.get_files(obj.query_media, obj.query_sort, obj.query_order, int(tag), filter=obj.query_fn_filter)
        self.clear()
        for q in sq:
            try:
                pb = Pixbuf.new_from_file_at_size(IMGPATH.format(q[0]), scale, scale)
            except GLib.Error:
                pb = missing
            self.append((*q[:-1], pb,))

    def set_query_filter_text(self, value):
        scale = self.scale
        missing = self.missing
        sq = Query.get_files('archives', 'filepath', 'desc', self.tag_id, filter=f'%{value}%')
        self.clear()
        for q in sq:
            try:
                pb = Pixbuf.new_from_file_at_size(IMGPATH.format(q[0]), scale, scale)
            except GLib.Error:
                pb = missing
            self.append((*q[:-1], pb,))


class AllViewStore(ViewStore):
    query_fn_filter = GObject.Property(type=str, default="")
    query_page = GObject.Property(type=int, default=1)
    query_sort = GObject.Property(type=str, default="mtime")
    query_order = GObject.Property(type=str, default="desc")
    query_media = GObject.Property(type=str, default="archives")
    query_code = GObject.Property(type=int, default=0)

    def __init__(self, scale):
        ViewStore.__init__(self, scale)

    def set_order(self, text):
        self.query_order = text.lower()
        self.load_store()

    def set_sort(self, text):
        self.query_sort = text.lower()
        self.load_store()

    def set_page(self, value):
        self.query_page = value
        self.load_store()

    def set_code(self, value):
        self.query_code = value
        self.load_store()

    def set_fn_filter(self, text):
        self.query_fn_filter = f"%{text}%"
        self.load_store()

    def load_store(self):
        missing = self.missing
        scale = self.scale

        if self.query_code == 0:
            sq = Query.get_all_files('archives', self.query_page, self.query_sort, self.query_order, self.query_fn_filter)
        elif self.query_code == 1:
            sq = Query.get_1tag_files('archives', self.query_page, self.query_sort,  self.query_order, self.query_fn_filter)
        elif self.query_code == -1:
            sq = Query.get_notag_files('archives', self.query_page, self.query_sort,  self.query_order, self.query_fn_filter)
        self.clear()
        for q in sq:
            try:
                pb = Pixbuf.new_from_file_at_size(IMGPATH.format(q[0]), scale, scale)
            except GLib.Error:
                pb = missing
            self.append((*q[:-1], pb,))
        


