from gi.repository import Gtk, GObject, Gdk, GLib
from models import Query
from humanfriendly import format_size
from clip import rethumb
from shell_commands import open_file, trash_file
from widgets import TagView
from data_models import tag_store


class FileEdit(Gtk.Grid):
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
    # __gsignals__ = {
    #     'backed': (GObject.SIGNAL_RUN_FIRST, None, ()),
    # }
    def __init__(self, file_id, alias):
        Gtk.Grid.__init__(self, row_spacing=5, column_spacing=5)
        self.set_property('margin-right', 5)
        self.set_property('margin-left', 5)
        # main_model.connect('type-changed', self.on_model_type_changed)
        # fe_model = FileEditModel()
        self.alias = alias
        self.t_model = Gtk.ListStore(int, str)
        self.r_model = Gtk.ListStore(int, str)
        # self.fe_model = fe_model

        # COMMANDS
        command_box = Gtk.Box.new(orientation=1, spacing=0)
        command_box.get_style_context().add_class("linked")
        self.attach(command_box, 0, 0, 1, 1)

        button = Gtk.Button('Open')
        button.connect('clicked', self.on_open_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button('Mcomix')
        button.connect('clicked', self.on_mcomix_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button('Open Folder')
        button.connect('clicked', self.on_openf_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button('Delete Entry')
        button.connect('clicked', self.on_del_entry_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button('Trash File & Entry')
        button.connect('clicked', self.on_del_file_entry_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button('Info List')
        button.connect('clicked', self.on_info_clicked)
        command_box.pack_start(button, False, True, 0)

        #FILE INFOS
        info_box = Gtk.Box.new(orientation=1, spacing=4)
        info_box.set_hexpand(True)
        self.attach(info_box, 1, 0, 1, 1)

        button = Gtk.Button()
        # button.set_halign(1)
        button.set_relief(2)
        img = Gtk.Image.new_from_file('')
        self.bind_property('imgfile', img, 'file', 0)
        button.set_image(img)
        button.connect('clicked', self.on_rethumb)
        info_box.pack_start(button, False, True, 0)

        label = Gtk.Label()
        self.bind_property('id', label, 'label', 0)
        label.set_halign(1)
        info_box.pack_start(label, False, True, 0)

        label = Gtk.Label()
        self.bind_property('filename', label, 'label', 0)
        label.set_halign(1)
        label.set_line_wrap(True)
        label.set_alignment(0,.5)
        label.set_selectable(True)
        info_box.pack_start(label, False, True, 0)

        label = Gtk.Label()
        self.bind_property('filepath', label, 'label', 0)
        label.set_line_wrap(True)
        label.set_halign(1)
        label.set_alignment(0,.5)
        label.set_selectable(True)
        info_box.pack_start(label, False, True, 0)

        label = Gtk.Label('size')
        self.bind_property('size', label, 'label', 0)
        label.set_halign(1)
        info_box.pack_start(label, False, True, 0)

        label = Gtk.Label('mtime')
        self.bind_property('mtime', label, 'label', 0)
        label.set_halign(1)
        info_box.pack_start(label, False, True, 0)

        entry = Gtk.Entry()
        self.bind_property('thumbpath', entry, 'text', 1)
        entry.set_placeholder_text('thumbpath')
        info_box.pack_start(entry, False, True, 0)

        entry = Gtk.Entry()
        entry.set_placeholder_text('set')
        self.bind_property('set', entry, 'text', 1)
        info_box.pack_start(entry, False, True, 0)

        entry = Gtk.Entry()
        entry.set_placeholder_text('note')
        self.bind_property('note', entry, 'text', 1)
        info_box.pack_start(entry, False, True, 0)

        entry = Gtk.SpinButton.new_with_range(0,100,1)
        entry.set_placeholder_text('rating')
        self.bind_property('rating', entry, 'value', 1)
        info_box.pack_start(entry, False, True, 0)

        button = Gtk.Button('Update')
        button.set_halign(1)
        button.connect('clicked', self.on_update)
        info_box.pack_start(button, False, True, 0)

        #TAGS
        tagbox = Gtk.Box.new(orientation=1, spacing=2)
        self.attach(tagbox, 2, 0, 1, 1)

        # label = Gtk.Label('Tags:')
        # tagbox.pack_start(label, False, True, 0)
        
        tagview = TagView()
        tagview.connect('tag-delete', self.on_tag_delete)
        tagview.connect('tag-read', self.on_tag_read)
        tagview.connect('tag-update', self.on_tag_update)
        tagview.set_model(self.t_model)
        # tagview.set_vexpand(True)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_property('shadow-type', 1)
        scrolled.add(tagview)
        tagbox.pack_start(scrolled, True, True, 0)

        hbox = Gtk.Box.new(orientation=0, spacing=0)
        hbox.get_style_context().add_class("linked")

        entry = Gtk.Entry()
        comp = Gtk.EntryCompletion()
        comp.set_text_column(1)
        comp.set_model(tag_store)
        entry.set_completion(comp)
        hbox.pack_start(entry, True, True, 0)

        button = Gtk.Button()
        img = Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.MENU)
        button.set_image(img)
        button.connect('clicked', self.on_add_tag_clicked, entry)
        hbox.pack_start(button, False, True, 0)

        tagbox.pack_start(hbox, False, True, 0)


        #RECOMMENDS
        label = Gtk.Label('Suggestions:')
        tagbox.pack_start(label, False, True, 0)
      
        tagview = TagView()
        tagview.connect('row-activated', self.on_recommend_activated)
        tagview.set_model(self.r_model)
        scrolled = Gtk.ScrolledWindow()
        # scrolled.set_hexpand(True)
        scrolled.set_vexpand(True)
        scrolled.set_property('shadow-type', 1)
        scrolled.add(tagview)
        tagbox.pack_start(scrolled, True, True, 0)

        #INFOBAR
        info = Gtk.InfoBar()
        message_label = Gtk.Label('Done')
        # info.
        info.connect('response', self.on_info_response, message_label)
        info.set_revealed(False)
        info.set_show_close_button(True)
        self.info = info
        c = info.get_content_area()
        c.add(message_label)
        self.attach(info, 0, 20, 3, 1)
        # box.pack_start(info, False, True, 0)

        self.set_file_id(file_id)

    # def on_model_type_changed(self, obj):
    #     if obj.query_type == QueryType.FILEUPDATE:
    #         self.set_file_id(obj.query_int)

    def on_info_response(self, info_bar, response_id, label):
        print(response_id)
        info_bar.set_revealed(True)
        if response_id == 1:
            label.set_label('Done')
            def close(*args):
                info_bar.set_revealed(False)
            GLib.timeout_add(2400, close, None)
        elif response_id == 2:
            label.set_label('Error')
        else:
            info_bar.set_revealed(False)


    def set_file_id(self, id):
        file = Query.get_file(id)
        try:
            self.imgfile = f'/media/soni/1001/persistent/1001/thumbs/{file.id}.jpg'
        except Exception as e:
            pass
        self.id = file.id
        self.filename = file.filename
        self.filepath = file.filepath
        self.size = format_size(file.size)
        self.mtime = str(file.mtime)
        self.thumbpath = file.thumb if file.thumb != None else ""
        self.set = file.set if file.set != None else ""
        self.note = file.note if file.note != None else ""
        self.rating = file.rating
        #
        self.t_model.clear()
        for q in Query.file_tags(id):
            self.t_model.append(q)
        self.r_model.clear()
        for q in Query.tag_findall(file.filename):
            self.r_model.append(q)

    def on_tag_read(self, widget):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        main_model.set_type(QueryType.TAG, model[iter][0], None)

    def on_tag_update(self, widget):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        main_model.set_type(QueryType.TAGUPDATE, model[iter][0], None)

    def on_tag_delete(self, widget):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        # model.remove_tag(iter)
        r = Query.delete_file_tag('archives', self.id, model[iter][0])
        if r:
            model.remove(iter)

    # def on_back_button_clicked(self, widget):
    #     self.emit('backed')

    def on_rethumb(self,widget):
        img = widget.get_image()
        item = Query.get_file(self.id)
        dest = rethumb(item, 'archives')
        print(dest)
        img.set_from_file(dest)

    def on_update(self, widget):
        r = Query.update_file(
            media='archives',
            index=self.id,
            thumb=self.thumbpath,
            set=self.set,
            note=self.note,
            rating=self.rating,
            )
        if r > 0: 
            self.info.set_message_type(0)
            self.info.response(1)
        else:
            self.info.set_message_type(3)
            self.info.response(2)

    def on_recommend_activated(self, widget, path, column):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        alias, tag_id, is_created = Query.add_file_tag('archives', self.id, tagname=model[iter][1])
        self.t_model.append((tag_id, alias,))

    def on_add_tag_clicked(self,widget, entry):
        text = entry.get_text()
        alias, tag_id, is_created = Query.add_file_tag('archives', self.id, tagname=text)
        self.t_model.append((tag_id, alias,))
        # fe_model.t_model.add_tag('archives', fe_model.id, text)
        entry.set_text("")

    def on_open_clicked(self,widget):
        open_file(self.filepath, 'default')

    def on_openf_clicked(self,widget):
        open_file(self.filepath, 'folder')

    def on_mcomix_clicked(self,widget):
        open_file(self.filepath, 'mcomix')

    def on_del_entry_clicked(self,widget):
        #DIALOG
        dialog = QuestionDialog(self, f"file_id: \'{self.id}\'")
        response = dialog.run()

        if response == Gtk.ResponseType.YES:
            r = Query.delete_file(self.id)
            if r:
                main_model.back()
        elif response == Gtk.ResponseType.NO:pass
        dialog.destroy()

    def on_del_file_entry_clicked(self,widget):
        #DIALOG
        dialog = QuestionDialog(self, f"file_id: \'{self.id}\', \'{self.filepath}\'")
        response = dialog.run()

        if response == Gtk.ResponseType.YES:
            r = trash_file(self.filepath)
            if not r:#0 success
                r = Query.delete_file(self.id)
                if r:
                    main_model.back()
        elif response == Gtk.ResponseType.NO:pass
        dialog.destroy()

    def on_info_clicked(self,widget):pass

