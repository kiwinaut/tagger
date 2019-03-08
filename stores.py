from gi.repository import Gtk, GObject, GLib
from gi.repository.GdkPixbuf import Pixbuf
from models import Query

import threading

class TagStore(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(
            self,
            int,     # 0 id
            str,     # 1 
            str,     # 2 
            str,     # 3 
            Pixbuf,  #4 thumb
        )

    def set_query_like_text(self, text):
        self.clear()
        for q in Query.get_tags_by_filter(text):
            try:
                pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[3]}.jpg', 128, 128)
            except GLib.Error:
                pb = None
            self.append((*q, pb,))

    def set_query_like_text_pb(self, text):
        self.clear()
        for q in Query.get_tags_by_filter(text):
            self.append((*q, None,))

        def foreach():
            def add_pb(model, path, iter, data):
                try:
                    pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{model[iter][3]}.jpg', 128, 128)
                except GLib.Error:
                    pb = None
                model[iter][4] = pb
            self.foreach(add_pb, None)

        foreach()
        
        # thread = threading.Thread(target=foreach)
        # thread.daemon = True
        # thread.start()

    def set_query_like_text_thread(self, text):
        self.clear()
        def appendrow():
            for q in Query.get_tags_by_filter(text):
                try:
                    pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[3]}.jpg', 64, 64)
                except GLib.Error:
                    pb = None
                # self.append((*q, pb,))
                GLib.idle_add(self.append, (*q, pb,))


        thread = threading.Thread(target=appendrow)
        thread.daemon = True
        thread.start()
        thread.join()

class ViewStore(Gtk.ListStore):
    def __init__(self):
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

    def append_from_query(self, query):
        for q in query:
            self.append(q)

    def set_query_tag_id(self, tag_id):
        sq = Query.get_files('archives', 'filepath', 'desc', tag_id)
        # sq = Query.get_files(obj.query_media, obj.query_sort, obj.query_order, int(tag), filter=obj.query_fn_filter)
        self.clear()
        for q in sq:
            try:
                pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[0]}.jpg', 192, 192)
            except GLib.Error:
                pb = None
            self.append((*q[:-1], pb,))
