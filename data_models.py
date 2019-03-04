from gi.repository import Gtk, GObject
from collections import deque
from gi.repository.GdkPixbuf import Pixbuf
from models import Query

avatar = Pixbuf.new_from_file_at_size('/usr/share/icons/Adwaita/256x256/status/avatar-default.png', 192, 192)

det_store = Gtk.ListStore(str, int, GObject.TYPE_UINT64)

tag_store = Gtk.ListStore(int, str, str, str)
tag_icon_store = Gtk.ListStore(int, str, Pixbuf)
tag_group_store = Gtk.ListStore(int, str, int)



class FileEditModel(GObject.GObject):
    id = GObject.Property(type=int)
    filepath = GObject.Property(type=str)
    filename = GObject.Property(type=str)
    mtime = GObject.Property(type=str)
    size = GObject.Property(type=str)
    thumbpath = GObject.Property(type=str)
    set = GObject.Property(type=str)
    note = GObject.Property(type=str)
    rating = GObject.Property(type=int)
    imgfile = GObject.Property(type=str)
    def __init__(self):
        GObject.GObject.__init__(self)
        self.t_model = Gtk.ListStore(int, str)
        self.r_model = Gtk.ListStore(int, str)

fe_model = FileEditModel()

class TagTreeStore(Gtk.TreeStore):
    def __init__(self):
        Gtk.TreeStore.__init__(self, int, str, str)

    def init(self, root_query):
        stack = []
        for q in root_query:
            if q[0] == 1:
                stack.append((None, '/'))
                # continue

            t = stack[-1]
            if q[1].startswith(t[1]):
                iter = self.append(t[0], q)
                stack.append((iter,q[1],))
            else:
                while True:
                    x = stack.pop()
                    # print(x[1], q[1])
                    if q[1].startswith(x[1]):
                        iter = self.append(x[0], q)
                        stack.append(x)
                        stack.append((iter,q[1],))
                        break
                    # else:
                    #     stack.append(x)

    def add_from_branch(self, parent_iter, parent_path, branch_query):
        stack = [(parent_iter, parent_path,)]
        for q in branch_query:
            # print(q)
            # if q[0] == 1:
            #     stack.append((None, '/'))
            #     continue

            t = stack[-1]
            if q[1].startswith(t[1]):
                iter = self.append(t[0],q)
                stack.append((iter,q[1],))
            else:
                while True:
                    x = stack.pop()
                    # print(x[1])
                    if q[1].startswith(x[1]):
                        iter = self.append(x[0],q)
                        stack.append(x)
                        stack.append((iter,q[1],))
                        break

col_store = TagTreeStore()

class FileTagsStore(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(self, int, str)

    def add_tag(self, media, file_id, value):
        alias, tag_id, is_created = Query.add_file_tag(media, file_id, tagname=value)
        self.append((tag_id, alias,))
        # emit tag-added  is-created

    def remove_tag(self, iter, media, file_id):
        r = Query.delete_file_tag(media, file_id, self[iter][0])
        if r:
            self.remove(iter)
        # emit tag-deleted


class TagEditModel(GObject.GObject):
    id = GObject.Property(type=int)
    name = GObject.Property(type=str)
    note = GObject.Property(type=str)
    rating = GObject.Property(type=int)
    thumb = GObject.Property(type=str)
    thumbpath = GObject.Property(type=str)
    def __init__(self):
        GObject.GObject.__init__(self)
        self.al_model = Gtk.ListStore(int, str)
        self.co_model = Gtk.ListStore(int, str)


ta_model = TagEditModel()

class ColModel(GObject.GObject):
    col = GObject.Property(type=int)
    __gsignals__ = {
        'col-changed': (GObject.SIGNAL_RUN_FIRST, None,(int,)),
        'folder-changed': (GObject.SIGNAL_RUN_FIRST, None,(int,))
    }   
    def __init__(self):
        GObject.GObject.__init__(self)

    def set_col(self, value):
        self.col = value
        self.emit('col-changed', self.col)

    def set_folder(self, value):
        self.folder = value
        self.emit('folder-changed', self.folder)

col_model = ColModel()

# class MainModel(GObject.GObject):
#     view = GObject.Property(type=str, default="listview")
#     media = GObject.Property(type=str, default='archives')
#     text = GObject.Property(type=str)
#     type = GObject.Property(type=str)
#     filter = GObject.Property(type=str, default="")
#     page = GObject.Property(type=int, default=1)
#     sort = GObject.Property(type=str, default="mtime")
#     order = GObject.Property(type=str, default="desc")
#     __gsignals__ = {
#         'reload': (GObject.SIGNAL_RUN_FIRST, None,())
#     }   
#     def __init__(self):
#         GObject.GObject.__init__(self)
#         self.connect("notify::type", self.on_type_notified)
#         self.v_model = None
#         self.back_stack = []
#         self.connect("notify::view", self.on_view_notified)

#     def reload(self):
#         self.emit('reload')

#     def on_type_notified(self, obj, gparamstring):
#         self.filter = ""

#     def on_view_notified(self, obj, gparamstring):
#         self.back_stack.append(obj.view)
#         print(obj.back_stack)

#     def back(self):
#         view = self.back_stack.pop()
#         view = self.back_stack.pop()
#         with self.freeze_notify():
#             self.view = view

class QueryType:
    TAG0 = 0
    TAG1 = 1
    TAG2 = 2
    TAGALL = 4
    TAG = 5
    TAGREAD = 10
    TAGUPDATE = 11
    FILEUPDATE = 12

class MainModel2(GObject.GObject):
    query_type = GObject.Property(type=int, default=-1)
    query_str = GObject.Property(type=str, default='')
    query_int = GObject.Property(type=int)
    query_fn_filter = GObject.Property(type=str, default="")
    query_page = GObject.Property(type=int, default=1)
    query_sort = GObject.Property(type=str, default="mtime")
    query_order = GObject.Property(type=str, default="desc")
    query_media = GObject.Property(type=str, default="archives")
    view = GObject.Property(type=str, default="listview")
    has_back = GObject.Property(type=bool, default=False)
    has_forw = GObject.Property(type=bool, default=False)

    __gsignals__ = {
        'type-changed': (GObject.SIGNAL_RUN_FIRST, None,()),
    }   
    def __init__(self):
        GObject.GObject.__init__(self)
        self.v_model = None
        self.back_stack = deque(maxlen=10)
        self.forw_stack = deque(maxlen=10)

    def set_type(self, type_, int_, str_):
        old_row = self.get_row()
        if old_row[0] >= 0:
            self.back_stack.append(old_row)
            
        # print('old:',self.get_row())
        self.has_back = True
        self.filter = ""
        self.query_int = int_
        self.query_str = str_
        self.query_type = type_
        self.emit('type-changed')

    def type_changed(self):
        self.emit('type-changed')

    def set_filter(self, value):
        self.query_fn_filter = value
        self.type_changed()

    def set_sort_and_order(self, sort, order):
        self.query_order = order
        self.query_sort = sort
        self.type_changed()

    def set_page(self, value):
        self.query_page = value
        self.type_changed()

    def get_row(self):
        return (
            self.query_type,
            self.query_str, 
            self.query_int, 
            self.query_fn_filter,
            self.query_sort,
            self.query_order,
            self.query_media,
            self.query_page
            )

    def set_row(self, row):
        with self.freeze_notify():
            (self.query_type,
            self.query_str, 
            self.query_int, 
            self.query_fn_filter,
            self.query_sort,
            self.query_order,
            self.query_media,
            self.query_page)=row

    def back(self):
        try:

            past_row = self.back_stack.pop()#error
            current_row = self.get_row()
            self.forw_stack.append(current_row)
            self.set_row(past_row)
            self.has_forw = True
            self.type_changed()
            # print(self.get_row())
            # print(self.back_stack, self.forw_stack)

        except IndexError:
            self.has_back = False

    def next(self):
        try:
            forw_row = self.forw_stack.pop()
            current_row = self.get_row()
            self.back_stack.append(current_row)
            self.set_row(forw_row)
            self.has_back = True
            self.type_changed()
            # print(self.get_row())
            # print(self.back_stack, self.forw_stack)
        except IndexError:
            self.has_forw = False

main_model = MainModel2()
