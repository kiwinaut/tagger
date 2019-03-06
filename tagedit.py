from gi.repository import Gtk, GObject, Gdk, GLib
from models import Query
from widgets import TagFlowBox, QuestionDialog
from data_models import tag_store


class TagEdit(Gtk.Overlay):
    id = GObject.Property(type=int)
    name = GObject.Property(type=str)
    note = GObject.Property(type=str)
    rating = GObject.Property(type=int)
    thumb = GObject.Property(type=str)
    thumbpath = GObject.Property(type=str)

    # __gsignals__ = {
    #     'backed': (GObject.SIGNAL_RUN_FIRST, None, ()),
    #     'list-tag': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    # }
    def __init__(self, tag_id, alias):
        Gtk.Overlay.__init__(self)
        c = self.get_style_context()
        c.add_class('editpage')

        rev = Gtk.Revealer()
        rev.set_reveal_child(False)
        self.rev = rev
        rev.add(Gtk.Label('none'))
        self.add_overlay(rev)

        #FILE INFOS
        info_box = Gtk.Box.new(orientation=1, spacing=4)
        info_box.set_hexpand(True)
        self.add(info_box)

        button = Gtk.Button()
        # button.set_halign(1)
        button.set_relief(2)
        img = Gtk.Image.new_from_file('')
        self.bind_property('thumbpath', img, 'file', 0)
        button.set_image(img)
        button.connect('clicked', self.on_rethumb)
        info_box.pack_start(button, False, True, 0)

        label = Gtk.Label()
        self.bind_property('id', label, 'label', 0)
        label.set_halign(1)
        info_box.pack_start(label, False, True, 0)


        entry = Gtk.Entry()
        self.bind_property('name', entry, 'text', 1)
        entry.set_placeholder_text('consistent tag name')
        info_box.pack_start(entry, False, True, 0)

        entry = Gtk.Entry()
        self.bind_property('thumb', entry, 'text', 1)
        entry.set_placeholder_text('thumb number')
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

        self.aliases = TagFlowBox()
        self.aliases.connect("child-deleted", self.on_alias_delete)
        self.aliases.connect("child-clicked", self.on_alias_delete)
        info_box.pack_start(self.aliases, False, True, 0)

        hbox = Gtk.Box.new(orientation=0, spacing=0)
        hbox.get_style_context().add_class("linked")

        entry = Gtk.Entry()
        comp = Gtk.EntryCompletion()
        comp.set_text_column(1)
        # comp.set_model(col_store)
        entry.set_completion(comp)
        hbox.pack_start(entry, True, True, 0)

        button = Gtk.Button()
        img = Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.MENU)
        button.set_image(img)
        button.connect('clicked', self.on_add_alias_clicked, entry)
        hbox.pack_start(button, False, True, 0)
        info_box.pack_start(hbox, False, True, 0)


        command_box = Gtk.Box.new(orientation=0, spacing=0)
        command_box.get_style_context().add_class("linked")

        button = Gtk.Button('List')
        button.connect('clicked', self.on_list_clicked)
        command_box.pack_start(button, False, True, 0)

        button = Gtk.Button('Delete')
        button.connect('clicked', self.on_del_clicked)
        command_box.pack_start(button, False, True, 0)
        info_box.pack_start(command_box, False, True, 0)



        self.set_tag_id(tag_id)

    def on_rethumb(self, widget):
        self.thumbpath = f'/media/soni/1001/persistent/1001/thumbs/{self.thumb}.jpg'



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


    def set_tag_id(self, id):
        file = Query.get_tag(id)
        self.id = file.id
        self.name = file.name if file.name != None else ""
        self.note = file.note if file.note != None else ""
        self.rating = file.rating
        self.thumb = file.thumb
        self.thumbpath = f'/media/soni/1001/persistent/1001/thumbs/{file.thumb}.jpg'
        #
        for q in Query.get_tag_aliases(self.id):
            self.aliases.add_tagchild(q[0],q[1])

    def on_alias_read(self, widget, *args):pass
        # selection = widget.get_selection()
        # model, iter = selection.get_selected()
        # main_model.view = "listview"

    def on_alias_delete(self, widget, child):
        #DIALOG
        dialog = QuestionDialog(self, f"alias_name: \'{child.label}\', alias_id: \'{child.id}\'")
        response = dialog.run()

        if response == Gtk.ResponseType.YES:
            if Query.remove_tag_alias(child.id):
                widget.remove(child)
                self.rev.set_reveal_child(True)
        elif response == Gtk.ResponseType.NO:pass
        dialog.destroy()

    def on_add_alias_clicked(self, widget, entry):
        text = entry.get_text()
        tag_id = self.id
        alias, alias_id, is_created = Query.add_tag_alias(tag_id, text)
        if is_created:
            pass
        self.aliases.add_tagchild(alias_id,alias)
        entry.set_text("")


    def on_update(self, widget):
        r = Query.update_tag(self.id, self.name, self.note, self.rating, self.thumb)
        if r > 0: 
            self.info.set_message_type(0)
            self.info.response(1)
        else:
            self.info.set_message_type(3)
            self.info.response(2)

    def on_list_clicked(self, widget):
        self.emit('list-tag', self.id)

    def on_del_clicked(self,widget):
        tag_id = self.id

        #DIALOG
        dialog = QuestionDialog(self, f"tag_id: \'{tag_id}\'")
        response = dialog.run()

        if response == Gtk.ResponseType.YES:
            if Query.delete_tag(tag_id):
                #TODO back?
                main_model.back()
        elif response == Gtk.ResponseType.NO:pass
        dialog.destroy()

