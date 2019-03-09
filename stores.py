from gi.repository import Gtk, GObject, GLib
from gi.repository.GdkPixbuf import Pixbuf
from models import Query

import threading, time

avatar = Pixbuf.new_from_file_at_size('/usr/share/icons/Adwaita/256x256/status/avatar-default.png', 32, 32)

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
        self.load_busy = False
        self.text_buf = []

    def set_query_from_folder(self, fol_int):
        self.clear()
        for q in Query.get_tags(fol_int):
            try:
                pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[3]}.jpg', 192, 192)
            except GLib.Error:
                pb = avatar
            self.append((*q, pb,))

    def set_query_like_text(self, text):
        self.clear()
        if text == "":
            return
        for q in Query.get_tags_by_filter(text):
            try:
                pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[3]}.jpg', 192, 192)
            except GLib.Error:
                pb = avatar
            self.append((*q, pb,))

    # def set_query_like_text_pb(self, text):
    #     if not self.load_busy:
    #         self.load_busy = True
    #         self.clear()
    #         for q in Query.get_tags_by_filter(text):
    #             self.append((*q, None,))

    #         def foreach():
    #             def add_pb(model, path, iter, data):
    #                 try:
    #                     pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{model[iter][3]}.jpg', 128, 128)
    #                 except GLib.Error:
    #                     pb = avatar
    #                     model.set_value(iter, 4, pb)
    #                 time.sleep(1)
    #             self.foreach(add_pb, None)

    #         # foreach()
    #         thread = threading.Thread(target=foreach)
    #         thread.daemon = True
    #         thread.start()
    #         self.load_busy = False
    #     else:
    #         self.text_buf.append(text)
    #     if self.text_buf:
    #         last = self.text_buf.pop()
    #         self.text_buf = []
    #         print(self.text_buf)
    #         self.set_query_like_text_pb(last)
        

    # def set_query_like_text_thread(self, text):
    #     self.clear()
    #     def appendrow():
    #         for q in Query.get_tags_by_filter(text):
    #             try:
    #                 pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[3]}.jpg', 64, 64)
    #             except GLib.Error:
    #                 pb = None
    #             # self.append((*q, pb,))
    #             GLib.idle_add(self.append, (*q, pb,))


    #     thread = threading.Thread(target=appendrow)
    #     thread.daemon = True
    #     thread.start()
    #     thread.join()

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
        self.tag_id = tag_id
        sq = Query.get_files('archives', 'filepath', 'desc', tag_id)
        # sq = Query.get_files(obj.query_media, obj.query_sort, obj.query_order, int(tag), filter=obj.query_fn_filter)
        self.clear()
        for q in sq:
            try:
                pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[0]}.jpg', 192, 192)
            except GLib.Error:
                pb = avatar
            self.append((*q[:-1], pb,))

    def set_query_filter_text(self, value):
        sq = Query.get_files('archives', 'filepath', 'desc', self.tag_id, filter=f'%{value}%')
        self.clear()
        for q in sq:
            try:
                pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[0]}.jpg', 192, 192)
            except GLib.Error:
                pb = avatar
            self.append((*q[:-1], pb,))

    def set_query_all_file_code(self, code):
        if code == 0:
            sq = Query.get_all_files('archives', 0, 'mtime', 'desc')
        elif code == 1:
            sq = Query.get_1tag_files('archives', 0, 'mtime',  'desc')
        elif code == -1:
            sq = Query.get_notag_files('archives', 0, 'mtime',  'desc')

        self.clear()
        for q in sq:
            try:
                pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[0]}.jpg', 192, 192)
            except GLib.Error:
                pb = avatar
            self.append((*q[:-1], pb,))
