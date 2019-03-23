from gi.repository import Gtk, Gdk, GObject
from config import CONFIG
from widgets.widgets import ViewSwitcher
from models import  Query
# from popovers import SciencePopOver
from data_models import QueryType, col_model, col_store, det_store
import shell_commands
from widgets.notebook import Notebook
from widgets.fileview import FileView, AllFileView
from widgets.fileedit import FileEdit
from widgets.instaview import InstaBox
from widgets.tagedit import TagEdit
from widgets.aliasesdirview import AliasesDirView
# viewstore = ViewStore()

class Window(Gtk.ApplicationWindow):
    scalefactor = GObject.Property(type=float, default=6.0)
    # __gsignals__ = {
    #   'scope-changed': (GObject.SIGNAL_RUN_FIRST, None, ()),
    # }
    def __init__(self, *args, **kwargs):
        Gtk.ApplicationWindow.__init__(self, *args, gravity=1, **kwargs)
        # self.set_border_width(0)
        self.set_default_size(900, 732)
        # self.tab_model = TabModel()
        # self.current_tab_model = TabModel()
        # self.bindings = {}

        # self.connect("delete-event", self.on_window_delete_event)
        # main_model.view = 'listview'
        # main_model.connect("notify::text", self.on_text_notified)
        # main_model.connect('type-changed', self.on_model_type_changed)
        notebook = Notebook()

        # clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        #HEADER BAR
        header = Gtk.HeaderBar()
        header.set_title("Tagger")
        header.set_subtitle(CONFIG['database.version'])
        header.set_show_close_button(True)
        # main_model.bind_property('query_media', header, 'title', 1)
        self.set_titlebar(header)

        box = Gtk.Box(orientation=0, spacing=0)
        box.get_style_context().add_class("linked")
        header.pack_start(box)

        menu_button = Gtk.MenuButton()
        menu = Gtk.Menu()
        read = Gtk.MenuItem.new_with_label('All Files')
        read.connect('activate', self.on_menu_all_files_activated, notebook)
        menu.append(read)
        read = Gtk.MenuItem.new_with_label('Untagged Files')
        read.connect('activate', self.on_menu_untagged_files_activated)
        menu.append(read)
        read = Gtk.MenuItem.new_with_label('One tag Files')
        read.connect('activate', self.on_menu_onetag_files_activated)
        menu.append(read)
        # read = Gtk.MenuItem.new_with_label('No Colection Tags')
        # read.connect('activate', self.on_menu_nocol_tags_activated)
        # menu.append(read)
        read = Gtk.MenuItem.new_with_label('All Tag Details')
        # read.connect('activate', self.on_menu_tags_details_activated)
        menu.append(read)
        read = Gtk.MenuItem.new_with_label('Insta Select')
        read.connect('activate', self.on_menu_insta_select_activated, notebook)
        menu.append(read)
        read = Gtk.MenuItem.new_with_label('Move and Vindex')
        read.connect('activate', self.on_menu_move_and_vindex_activated)
        menu.append(read)
        menu_button.set_popup(menu)
        menu.show_all()
        box.pack_start(menu_button, False, True, 0)


        box = Gtk.Box(orientation=0, spacing=4)
        header.pack_end(box)

        #SCIENCE
        science = Gtk.Popover()
        self.set_position(Gtk.PositionType.BOTTOM)
        sbox = Gtk.Box.new(orientation=1, spacing=0)
        sbox.set_property('margin',18)
        science_adjustment = Gtk.Adjustment.new(6.0, 1.0, 8.0, 1.0, 10.0, 0)
        self.scale_adjust = science_adjustment
        thumb_scaler = Gtk.Scale.new(0, science_adjustment)
        thumb_scaler.set_size_request(180, -1)
        thumb_scaler.set_digits(0)
        thumb_scaler.connect('format-value', self.on_format_value)
        sbox.pack_start(thumb_scaler, False, True, 0)
        sbox.show_all()
        science.add(sbox)
        #
        image = Gtk.Image.new_from_icon_name("applications-science-symbolic", Gtk.IconSize.MENU)
        button = Gtk.MenuButton(image=image)
        button.set_popover(science)
        box.pack_end(button, False, True, 0)
        #
        #
        # VIEWSWITCHER
        view_swicher = ViewSwitcher()
        self.viewsw = view_swicher
        box.pack_start(view_swicher, False, False, 0)
        #
        #
        box = Gtk.Box.new(orientation=1, spacing=0)
        self.add(box)

        science_adjustment.connect('value-changed', self.science_value_changed, notebook)
        view_swicher.connect('switched', self.on_view_switched, notebook)
        notebook.connect('switch-page', self.on_notebook_switch_page, view_swicher, science_adjustment, thumb_scaler)

        box.pack_start(notebook, True, True, 0)

        screen = Gdk.Screen.get_default()
        # css_provider = Gtk.CssProvider.get_named('Adwaita', 'dark')
        css_provider_file = Gtk.CssProvider()
        css_provider_file.load_from_path(CONFIG['static'].format('main.css'))
        context = Gtk.StyleContext()
        # # context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        context.add_provider_for_screen(screen, css_provider_file, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.show_all()
        # main_model.view = 'listview'
        self.init_sets()
        self.set_icon_from_file(CONFIG['static'].format('tagger.png'))
        # alias_entry.grab_focus()

        adv = AliasesDirView()
        adv.connect('file-list', self.on_file_list)
        adv.connect('tag-edit', self.on_tag_edit)
        # self.bind_property('scalefactor', adv, 'scalefactor', 0)
        num = notebook.append_static(adv,'Search')
        notebook.set_current_page(num)
        self.notebook = notebook

    # def on_sstack_key_pressed(self, widget, event, science):
    #     science.popup()
    #     science.file_search.grab_focus()
    #     science.file_search.set_text(event.string)
    #     science.file_search.set_position(-1)

    # def on_group_combo_changed(self, widget):
    #     tree_iter = widget.get_active_iter()
    #     if tree_iter is not None:
    #         model = widget.get_model()
    #         country = model[tree_iter][0]
    #         print("Selected: country=%s" % country)

    def on_menu_tags_details_activated(self, widget):
        det_store.clear()
        qu = Query.get_tag_details('archives')
        for q in qu:
            det_store.append(q)
        self.stack.set_visible_child_full('detail', 0)

    def on_format_value(self, scale, value):
        return f'{int(value*32)}px'

    def science_value_changed(self, widget, notebook):
        num = notebook.get_current_page()
        child = notebook.get_nth_page(num)
        child.set_scale(widget.get_value())
        print('set child scale=',child.get_scale())

    def on_view_switched(self, widget, notebook):
        num = notebook.get_current_page()
        child = notebook.get_nth_page(num)
        child.set_view(widget.view)

    def on_notebook_switch_page(self, notebook, page, page_num, view, adj, scaler):
        try:
            value = page.get_view()
            print('get view=',value)
            view.set_sensitive(True)
            view.set_property('view', value)
        except:
            view.set_sensitive(False)

        try:
            value = page.get_scale()
            print('get adj=',value)
            scaler.set_sensitive(True)
            adj.set_property('value', value)
        except:
            scaler.set_sensitive(False)




    # def on_tag_edit_list_tag(self, widget, tag_id, tag_label):
    #     tag_edit = TagEdit()
    #     # tag_edit.connect('list-tag', self.on_tag_edit_list_tag)
    #     num = self.notebook.append_buttom(tag_edit, 'edit')
    #     self.notebook.set_current_page(num)

    def on_menu_insta_select_activated(self, widget, notebook):
        i = InstaBox()
        i.show_all()
        # f_edit.connect('tag-edit', self.on_tag_edit)
        num = notebook.append_buttom(i, 'insta', 'edit')
        notebook.set_current_page(num)

    def on_menu_move_and_vindex_activated(self, widget):
        shell_commands.movetotemp()

    def on_tag_filenames(self, widget, tag_id, clipboard):
        res = Query.get_tag_column(tag_id)
        clipboard.set_text(res, -1)

    def on_menu_all_files_activated(self, widget, notebook):
        print('allfiles',
            self.scale_adjust.get_property('value'),
            self.viewsw.get_property('view'),

            )
        fw = AllFileView(
            self.scale_adjust.get_property('value'),
            self.viewsw.get_property('view'),
            0
            )
        fw.connect('file-edit', self.on_file_edit)
        # self.bind_property('scalefactor', fw, 'scalefactor', 0)
        num = notebook.append_buttom(fw, 'All Files', 'all-file-list')
        notebook.set_current_page(num)

    def on_menu_untagged_files_activated(self, widget):
        fw = AllFileView(
            self.scale_adjust.get_property('value'),
            self.viewsw.get_property('view'),
            -1
            )
        fw.connect('file-edit', self.on_file_edit)
        num = self.notebook.append_buttom(fw, 'Untagged Files', 'all-file-list')
        self.notebook.set_current_page(num)

    def on_menu_onetag_files_activated(self, widget):
        fw = AllFileView(
            self.scale_adjust.get_property('value'),
            self.viewsw.get_property('view'),
            1
            )
        fw.connect('file-edit', self.on_file_edit)
        num = self.notebook.append_buttom(fw, '1 Tag Files', 'all-file-list')
        self.notebook.set_current_page(num)

    # def on_menu_nocol_tags_activated(self, widget):
    #     tag_store.clear()
    #     for q in Query.get_tags():
    #         tag_store.append(q)

    def on_view_notified(self, obj, gparamstring, stack):
        stack.set_visible_child_full(obj.view, 0)

    def on_file_edit(self, widget, file_id, alias):
        f_edit = FileEdit(file_id, alias)
        f_edit.show_all()
        f_edit.connect('tag-edit', self.on_tag_edit)
        num = self.notebook.append_buttom(f_edit,alias, 'edit')
        self.notebook.set_current_page(num)

    # def on_tag_filter_changed(self, widget):
    #     text = widget.get_text()
    #     tag_store.clear()
    #     for q in Query.get_tags_by_filter(text):
    #         tag_store.append(q)

    def on_col_read_activated(self, widget, *args):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        col_model.set_col(model[iter][0])
   
    def on_folder_read_activated(self, widget, *args):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        col_model.set_folder(model[iter][0])
   
    # def on_tag_read_smart(self, widget, *args):
    #     selection = widget.get_selection()
    #     model, iter = selection.get_selected()
    #     main_model.set_type(QueryType.TAG, model[iter][0], None)
        
    def on_tag_read(self, widget, *args):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        self.on_file_list(widget, model[iter][0], model[iter][1])

    def on_file_list(self, widget, tag_id, tag_name):
        fw = FileView(
            tag_id, 
            tag_name, 
            self.scale_adjust.get_property('value'),
            self.viewsw.get_property('view'),
            )
        fw.connect('file-edit', self.on_file_edit)
        num = self.notebook.append_buttom(fw,tag_name,'file-list')
        self.notebook.set_current_page(num)

    def on_tag_edit(self, widget, tag_id, tag_name):
        # selection = widget.get_selection()
        # model, iter = selection.get_selected()
        tag_edit = TagEdit(tag_id, tag_name)
        tag_edit.show_all()
        tag_edit.connect('file-list', self.on_file_list)
        num = self.notebook.append_buttom(tag_edit, tag_name, 'edit')
        self.notebook.set_current_page(num)

    def init_sets(self):
        # for q in Query.get_cols():
        #     col_store.append(q)
        col_store.init(Query.get_tree())

        # for q in Query.get_tags(-1):
        #     tag_store.append(q)

    def on_window_delete_event(self, widget, event):
        Gtk.main_quit()