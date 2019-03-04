from gi.repository import Gtk, GObject
# from widgets import GroupChangeRadios
# import cell_functions
# from enums import SortBy, SortOrder, Mime, FieldType


gstore, nstore = None, None


class SciencePopOver(Gtk.Popover):
    __gsignals__ = {
        'sort-changed': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        # 'sortorder-changed': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        # 'filter-changed': (GObject.SIGNAL_RUN_FIRST, None, (object, bool)),
        # 'isnone-changed': (GObject.SIGNAL_RUN_FIRST, None, (object, bool)),
        'filename-filter-changed': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
    }
    def __init__(self):
        Gtk.Popover.__init__(self)
        # self.set_pointing_to(rect)
        # self.set_relative_to(relative)
        self.set_position(Gtk.PositionType.BOTTOM)

        box = Gtk.Box.new(orientation=1, spacing=0)
        box.set_property('margin',18)

        grid = Gtk.Grid(row_spacing=0, column_spacing=15)


        radio = Gtk.RadioButton.new_with_label(None, 'Set     A-Z')
        radio.set_halign(1)
        radio.set_active(True)
        radio.connect("toggled", self.on_sortby_radio_toggled, "set,asc")
        grid.attach(radio, 0, 2, 1, 1)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.set_label("Set     Z-A")
        radio.connect("toggled", self.on_sortby_radio_toggled, "set,desc")
        grid.attach(radio, 0, 3, 1, 1)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.set_label("Count    1-9")
        radio.connect("toggled", self.on_sortby_radio_toggled, "count,asc")
        grid.attach(radio, 0, 4, 1, 1)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.set_label("Count    9-1")
        radio.connect("toggled", self.on_sortby_radio_toggled, "count,desc")
        grid.attach(radio, 0, 5, 1, 1)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.set_label("Mtime    1-9")
        radio.connect("toggled", self.on_sortby_radio_toggled, "mtime,asc")
        grid.attach(radio, 0, 6, 1, 1)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.set_label("Mtime    9-1")
        radio.connect("toggled", self.on_sortby_radio_toggled, "mtime,desc")
        grid.attach(radio, 0, 7, 1, 1)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.set_label("Size     1-9")
        radio.connect("toggled", self.on_sortby_radio_toggled, "size,asc")
        grid.attach(radio, 0, 8, 1, 1)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.set_label("Size     9-1")
        radio.connect("toggled", self.on_sortby_radio_toggled, "size,desc")
        grid.attach(radio, 0, 9, 1, 1)

        sepa = Gtk.Separator()
        grid.attach(sepa, 0, 19, 1, 1)

        # order
        entry = Gtk.SearchEntry()
        self.file_search = entry
        entry.connect('activate', self.on_extra_changed)
        grid.attach(entry, 0, 29, 1, 1)

        # radio = Gtk.RadioButton.new_with_label(None, 'Set Like')
        # radio.connect("toggled", self.on_extra_filter_col_toggled)
        # radio.set_halign(1)
        # grid.attach(radio, 3, 3, 1, 1)

        # radio = Gtk.RadioButton.new_from_widget(radio)
        # radio.connect("toggled", self.on_extra_filter_col_toggled)
        # radio.set_label("Filename Like")
        # entry.connect('changed', self.on_extra_changed, radio)
        # grid.attach(radio, 3, 4, 1, 1)


        box.pack_start(grid, True, True, 0)
        box.show_all()

        self.add(box)

    def on_extra_changed(self, widget):
        text = widget.get_text()
        self.emit('filename-filter-changed', text)

    def on_sortby_radio_toggled(self, widget, sort_string):
        if widget.get_active():
            self.emit('sort-changed', sort_string)

    # def on_sortorder_radio_toggled(self, widget, enum):
    #     if widget.get_active():
    #         self.emit('sortorder-changed', enum)

    # def on_filter_toggled(self, widget, col):
    #     self.emit('filter-changed', col, widget.get_active())

    # def on_isnone_toggled(self, widget, enum):
    #     self.emit('isnone-changed', enum, widget.get_active())

    def on_extra_filter_col_toggled(self, widget, col, entry):
        if widget.get_active():
            value = entry.get_text().strip()
            if value:
                self.emit('extra-changed', col, value)

class IconPopOver(Gtk.Popover):
    def __init__(self, relative):
        Gtk.Popover.__init__(self)
        # self.set_pointing_to(rect)
        self.set_relative_to(relative)
        self.set_position(Gtk.PositionType.BOTTOM)

        box = Gtk.Box.new(orientation=1, spacing=0)
        box.set_property('margin',8)

        scale = Gtk.Scale.new_with_range(orientation=0,min=1,max=4,step=1)
        scale.set_draw_value(False)
        scale.set_has_origin(False)
        scale.add_mark(1, 3, None)
        scale.add_mark(2, 3, None)
        scale.add_mark(3, 3, None)
        scale.add_mark(4, 3, None)
        scale.set_size_request(140,-1)
        self.scale =scale

        box.pack_start(scale, True, True, 0)

        sepa = Gtk.Separator()
        sepa.set_property('margin-top',5)
        sepa.set_property('margin-bottom',5)
        box.pack_start(sepa, True, True, 0)


        label = Gtk.Label()
        label.set_markup('<span color=\"grey\"><b>Sort</b></span>')
        label.set_property('halign',1)
        label.set_property('margin-left',8)
        box.pack_start(label, False, False, 0)


        radio = Gtk.RadioButton.new_with_label(None, 'Filename')
        radio.sid = 12
        self.radios = []
        self.radios.append(radio)
        box.pack_start(radio, False, False, 0)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.set_label('Set')
        radio.sid = 4
        self.radios.append(radio)
        box.pack_start(radio, False, False, 0)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.set_label('Size')
        radio.sid = 8
        self.radios.append(radio)
        box.pack_start(radio, False, False, 0)

        radio = Gtk.RadioButton.new_from_widget(radio)
        radio.sid = 7
        radio.set_label('Last Modified')
        self.radios.append(radio)
        box.pack_start(radio, False, False, 0)

        sepa = Gtk.Separator()
        sepa.set_property('margin-top',5)
        sepa.set_property('margin-bottom',5)
        box.pack_start(sepa, True, True, 0)

        toggle = Gtk.CheckButton.new_with_label('Reverse')
        self.reverse = toggle
        box.pack_start(toggle, False, False, 0)

        sepa = Gtk.Separator()
        sepa.set_property('margin-top',5)
        sepa.set_property('margin-bottom',5)
        box.pack_start(sepa, True, True, 0)

        label = Gtk.Label()
        label.set_markup('<span color=\"grey\"><b>Filter</b></span>')
        label.set_property('halign',1)
        label.set_property('margin-left',8)
        box.pack_start(label, False, False, 0)

        toggle = Gtk.CheckButton.new_with_label('Archive')
        toggle.set_active(True)
        self.archive = toggle
        box.pack_start(toggle, False, False, 0)

        toggle = Gtk.CheckButton.new_with_label('LibImage')
        toggle.set_active(True)
        self.libimage = toggle
        box.pack_start(toggle, False, False, 0)

        toggle = Gtk.CheckButton.new_with_label('Video')
        toggle.set_active(True)
        self.video = toggle
        box.pack_start(toggle, False, False, 0)


        box.show_all()

        self.add(box)

class ThumbPopOver(Gtk.Popover):
    def __init__(self, widget):
        Gtk.Popover.__init__(self)
        self.set_relative_to(widget)
        # self.set_pointing_to(rect)

        self.set_position(Gtk.PositionType.LEFT)

        img = Gtk.Image()
        self.add(img)
        img.show_all()

    def set_image(self, pixbuf):
        self.get_child().set_from_pixbuf(pixbuf)

search_model = Gtk.ListStore(int, str)
search_model.append((0,'hhhhhh',))
search_model.append((2,'hhhh',))
search_model.append((4,'hhhhh',))



class QuickSearch(Gtk.Popover):
    __gsignals__ = {
        'added': (GObject.SIGNAL_RUN_FIRST, None, (object, str)),
    }
    def __init__(self, widget):
        Gtk.Popover.__init__(self)
        self.set_relative_to(widget)
        self.set_position(Gtk.PositionType.BOTTOM)

        box = Gtk.Box.new(orientation=1, spacing=5)
        box.set_property('margin', 5)

        entry = Gtk.Entry()
        entry.set_property('activates-default',True)
        # entry.grab_focus()
        entry.set_can_default(False)
        self.entry = entry

        search_comp = Gtk.EntryCompletion()
        search_comp.set_model(search_model)
        search_comp.set_text_column(1)

        renderer = Gtk.CellRendererPixbuf()
        search_comp.pack_start(renderer, False)
        search_comp.connect('match-selected', self.on_match_selected)
        # self.search_comp.add_attribute(renderer, 'pixbuf', 1)
        # search_comp.set_cell_data_func(renderer, cell_functions.coltype_cell_data_func, func_data=None)

        renderer = Gtk.CellRendererText()
        renderer.set_property('font','8')
        renderer.set_property('foreground','grey')
        search_comp.pack_start(renderer, False)
        # search_comp.set_cell_data_func(renderer, cell_functions.coltype_str_cell_data_func, func_data=None)
        # self.search_comp.add_attribute(renderer, 'text', 2)

        entry.set_completion(search_comp)

        box.pack_start(entry, True, True, 0)

        button = Gtk.Button("Add")
        button.get_style_context().add_class('suggested-action')
        button.connect('clicked', self.on_button_clicked, entry)
        button.set_halign(2)#end
        button.set_can_default(True)
        # button.grab_default()
        box.pack_start(button, False, False, 0)
        self.add(box)
        self.set_default_widget(button)
        box.show_all()

    def on_match_selected(self, entry_completion, model, iter):
        entry = entry_completion.get_entry()
        entry.col_type = model[iter][0]
        entry.value = model[iter][1]

    def set_tag_widget(self, widget):
        self.tag_widget = widget

    def set_text(self, label):
        self.entry.set_text(label)

    def set_model_iter(self, model, iter):
        self.model = model
        self.iter = iter

    def on_button_clicked(self, widget, entry):
        # col = entry.get_text().strip()
        # if t != "" or t is not None:
        # self.emit('added', entry.col_type, entry.value)
        self.tag_widget.set_text(entry.value)
        self.tag_widget.set_col_type(entry.col_type)
        self.popdown()

class UpdatePopOver(Gtk.Popover):
    __gsignals__ = {
        'update': (GObject.SIGNAL_RUN_FIRST, None, (str,object,object)),
    }
    def __init__(self, widget):
        Gtk.Popover.__init__(self)
        self.set_relative_to(widget)
        self.set_position(Gtk.PositionType.BOTTOM)

        box = Gtk.Box.new(orientation=1, spacing=5)
        box.set_property('margin', 5)

        entry = Gtk.Entry()
        entry.set_property('activates-default',True)
        # entry.grab_focus()
        entry.set_can_default(False)
        self.entry = entry
        box.pack_start(entry, True, True, 0)

        button = Gtk.Button("Update")
        button.get_style_context().add_class('suggested-action')
        button.connect('clicked', self.on_button_clicked, entry)
        button.set_halign(2)#end
        button.set_can_default(True)
        self.set_default_widget(button)
        # button.grab_default()
        box.pack_start(button, False, False, 0)
        self.add(box)
        box.show_all()

    def set_text(self, label):
        self.entry.set_text(label)

    def set_model_iter(self, model, iter):
        self.model = model
        self.iter = iter

    def on_button_clicked(self, widget, entry):
        t = entry.get_text().strip()
        if t != "" or t is not None:
            self.emit('update', t, self.model, self.iter)
        self.popdown()

class RenamePopOver(UpdatePopOver):
    def __init__(self, widget):
        UpdatePopOver.__init__(self, widget)
        comp = Gtk.EntryCompletion()
        comp.set_model(nstore)
        comp.set_text_column(0)
        self.entry.set_completion(comp)



class RegroupPopOver(UpdatePopOver):
    def __init__(self, widget):
        UpdatePopOver.__init__(self, widget)
        box = self.get_child()

        comp = Gtk.EntryCompletion()
        comp.set_model(gstore)
        comp.set_text_column(0)
        self.entry.set_completion(comp)

        radio_group = GroupChangeRadios()
        radio_group.set_completion(comp)
        box.pack_start(radio_group, False, False, 0)
        box.reorder_child(radio_group, 1)

        box.show_all()





