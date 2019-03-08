from gi.repository import Gtk, GObject, GLib
from models import Query
from humanfriendly import format_size
from clip import rethumb
from shell_commands import open_file, trash_file
# from widgets import TagView
# from data_models import tag_store
from .widgets import QuestionDialog
from .tagflowbox import TagFlowBox


class FileEdit(Gtk.Overlay):
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
    __gsignals__ = {
        'tag-edit': (GObject.SIGNAL_RUN_FIRST, None, (int, str,)),
    }
    def __init__(self, file_id, alias):
        Gtk.Overlay.__init__(self)
        self.alias = alias

        c = self.get_style_context()
        c.add_class('editpage')

        rev = Gtk.Revealer()
        rev.set_halign(3)
        rev.set_valign(1)
        self.rev = rev
        box = Gtk.Box.new(orientation=0, spacing=4)
        c = box.get_style_context()
        c.add_class('app-notification')
        label = Gtk.Label('mmessage')
        self.msglabel = label
        box.pack_start(label, False, True, 0)
        rev.add(box)


        #FILE INFOS
        info_box = Gtk.Box.new(orientation=1, spacing=4)
        info_box.set_hexpand(True)
        self.add(info_box)
        self.add_overlay(rev)

        button = Gtk.Button()
        # button.set_halign(1)
        button.set_relief(2)
        img = Gtk.Image.new_from_file('')
        self.bind_property('imgfile', img, 'file', 0)
        button.set_image(img)
        button.connect('clicked', self.on_rethumb_button_clicked)
        info_box.pack_start(button, False, True, 0)

        #COMMANDS
        command_box = Gtk.Box.new(orientation=0, spacing=0)
        command_box.get_style_context().add_class("linked")

        button = Gtk.Button.new_from_icon_name('applications-system', 2)
        button.set_tooltip_text('Open')
        button.connect('clicked', self.on_open_button_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button('🐵')
        button.set_tooltip_text('Mcomix')
        button.connect('clicked', self.on_mcomix_button_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button.new_from_icon_name('folder', 2)
        button.set_tooltip_text('Open Folder')
        button.connect('clicked', self.on_openf_button_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button.new_from_icon_name('emblem-unreadable', 2)
        button.set_tooltip_text('Delete Entry')
        button.connect('clicked', self.on_del_entry_button_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button.new_from_icon_name('user-trash', 2)
        button.set_tooltip_text('Trash File & Entry')
        button.connect('clicked', self.on_del_file_entry_button_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button.new_from_icon_name('system-search', 2)
        button.set_tooltip_text('Info List')
        # button.connect('clicked', self.on_info_clicked)

        command_box.pack_start(button, False, True, 0)
        info_box.pack_start(command_box, False, True, 0)
        #


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
        button.connect('clicked', self.on_update_button_clicked)
        info_box.pack_start(button, False, True, 0)

        #TAGS
        self.tags_container = TagFlowBox()
        self.tags_container.connect("child-deleted", self.on_tag_container_child_deleted)
        self.tags_container.connect("child-clicked", self.on_tag_container_child_clicked)
        info_box.pack_start(self.tags_container, False, True, 0)

        hbox = Gtk.Box.new(orientation=0, spacing=0)
        hbox.get_style_context().add_class("linked")

        entry = Gtk.Entry()
        comp = Gtk.EntryCompletion()
        comp.set_text_column(1)
        # comp.set_model(col_store) #TODO
        entry.set_completion(comp)
        hbox.pack_start(entry, True, True, 0)

        button = Gtk.Button()
        img = Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.MENU)
        button.set_image(img)
        entry.connect('activate', self.on_add_tag_entry_activated, button)
        button.connect('clicked', self.on_add_tag_button_clicked, entry)
        hbox.pack_start(button, False, True, 0)
        info_box.pack_start(hbox, False, True, 0)

        #RECOMMENDS
        self.rcmmnds_container = TagFlowBox()
        self.rcmmnds_container.connect("child-clicked", self.on_rcmmnds_child_clicked)
        info_box.pack_start(self.rcmmnds_container, False, True, 0)


        self.set_file_id(file_id)


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
        for q in Query.file_tags(id):
            self.tags_container.add_tagchild(q[0],q[1])
        for q in Query.tag_findall(file.filename):
            self.rcmmnds_container.add_sggstchild(q[0],q[1])


    def on_rethumb_button_clicked(self,widget):
        img = widget.get_image()
        item = Query.get_file(self.id)
        dest = rethumb(item, 'archives')
        print(dest)
        img.set_from_file(dest)

    def on_update_button_clicked(self, widget):
        try:
            r = Query.update_file(
                media='archives',
                index=self.id,
                thumb=self.thumbpath,
                set=self.set,
                note=self.note,
                rating=self.rating,
                )
            self.show_message('Done', r)
        except:
            self.show_message('Error', 0)


    #REVELAER
    def show_message(self, message, r):
        self.msglabel.set_label(message)
        box = self.msglabel.get_parent()
        sc = box.get_style_context()
        if r > 0:
            sc.add_class('app-notification-ok')
        else:
            sc.add_class('app-notification-error')

        self.rev.set_reveal_child(True)
        def close(*args):
            self.rev.set_reveal_child(False)
            sc.remove_class('app-notification-ok')
            sc.remove_class('app-notification-error')
        GLib.timeout_add(2400, close, None)

    #COMMANDS
    def on_open_button_clicked(self,widget):
        open_file(self.filepath, 'default')

    def on_openf_button_clicked(self,widget):
        open_file(self.filepath, 'folder')

    def on_mcomix_button_clicked(self,widget):
        open_file(self.filepath, 'mcomix')

    def on_del_entry_button_clicked(self,widget):
        #DIALOG
        dialog = QuestionDialog(self, f"file_id: \'{self.id}\'")
        response = dialog.run()

        if response == Gtk.ResponseType.YES:
            r = Query.delete_file(self.id)
            if r:
                main_model.back()
        elif response == Gtk.ResponseType.NO:pass
        dialog.destroy()

    def on_del_file_entry_button_clicked(self,widget):
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

    #TAGS CONTAINER
    def on_tag_container_child_clicked(self, widget, child):
        self.emit('file-list', child.id, child.label)

    def on_tag_container_child_deleted(self, widget, child):
        #DIALOG
        dialog = QuestionDialog(self, f"alias_name: \'{child.label}\', alias_id: \'{child.id}\'")
        response = dialog.run()

        if response == Gtk.ResponseType.YES:
            r = Query.delete_file_tag('archives', self.id, child.id)
            if r > 0:
                widget.remove(child)
                self.show_message('Done', r)
            else:
                self.show_message('Error', r)
                
        elif response == Gtk.ResponseType.NO:pass
        dialog.destroy()

    def on_add_tag_entry_activated(self, widget, button):
        button.clicked()

    def on_add_tag_button_clicked(self, widget, entry):
        text = entry.get_text()
        file_id = self.id
        alias, tag_id, is_created = Query.add_file_tag('archives', file_id, tagname=text)
        if is_created:
            pass
        self.tags_container.add_tagchild(tag_id, alias)
        self.show_message('Done', 1)
        entry.set_text("")

    #RECOMMENDS
    def on_rcmmnds_child_clicked(self, widget, child):
        alias, tag_id, is_created = Query.add_file_tag('archives', self.id, tagname=child.label)
        self.tags_container.add_tagchild(tag_id, alias)
        self.show_message('Done', 1)
