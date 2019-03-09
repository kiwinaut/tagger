from gi.repository import Gtk, Gdk, GLib
from config import CONFIG
from widgets.widgets import ViewSwitcher, IconView, HistorySwitcher, MediaSwitcher, DetailView, TagTreeView
from dirview import TagStore, CollectionView, ColStore
from icon_list_view import ViewStore, ListView
from models import Collections, Tags, Aliases, TagCollections, Query
from gi.repository.GdkPixbuf import Pixbuf
from popovers import SciencePopOver
from data_models import main_model, QueryType, col_model, col_store,  tag_icon_store, det_store, tag_group_store, avatar
import shell_commands
from widgets.notebook import Notebook
from widgets.fileview import FileView
from widgets.fileedit import FileEdit
from widgets.tagedit import TagEdit
from widgets.aliasesdirview import AliasesDirView

viewstore = ViewStore()



class Window(Gtk.ApplicationWindow):
    # __gsignals__ = {
    #   'scope-changed': (GObject.SIGNAL_RUN_FIRST, None, ()),
    # }
    def __init__(self, *args, **kwargs):
        Gtk.ApplicationWindow.__init__(self, *args, gravity=1, **kwargs)
        # self.set_border_width(0)
        self.set_default_size(900, 732)
        self.connect("delete-event", self.on_window_delete_event)
        # main_model.view = 'listview'
        # main_model.connect("notify::text", self.on_text_notified)
        # main_model.connect('type-changed', self.on_model_type_changed)

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
        read.connect('activate', self.on_menu_all_files_activated)
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
        read.connect('activate', self.on_menu_tags_details_activated)
        menu.append(read)
        read = Gtk.MenuItem.new_with_label('Move and Vindex')
        read.connect('activate', self.on_menu_move_and_vindex_activated)
        menu.append(read)
        menu_button.set_popup(menu)
        menu.show_all()
        box.pack_start(menu_button, False, True, 0)

        # image = Gtk.Image.new_from_icon_name("view-refresh-symbolic", Gtk.IconSize.MENU)
        # button = Gtk.Button(image=image)
        # # button.connect('clicked', self.on_index_clicked)
        # box.pack_start(button, False, True, 0)

        # hist = HistorySwitcher()
        # header.pack_start(hist)

        # medi = MediaSwitcher()
        # header.pack_start(medi)


        box = Gtk.Box(orientation=0, spacing=4)
        header.pack_end(box)

        # image = Gtk.Image.new_from_icon_name("applications-science-symbolic", Gtk.IconSize.MENU)
        # button = Gtk.MenuButton(image=image)
        # science = SciencePopOver()
        # science.connect('sort-changed', self.on_science_sort_changed)
        # science.connect('filename-filter-changed', self.on_science_filename_filter_changed)
        # science.set_relative_to(button)
        # button.set_popover(science)
        # box.pack_end(button, False, True, 0)

        # spin_button = Gtk.SpinButton.new_with_range(1,9999,1)
        # # entry.set_size_request(20,12)
        # spin_button.set_property('width-request', 20)
        # spin_button.set_property('value', main_model.query_page)
        # spin_button.connect('value-changed', self.on_page_changed)
        # # main_model.bind_property('query_page', spin_button, 'value', 1)
        # box.pack_start(spin_button, False, False, 0)

        sw = ViewSwitcher()
        sw.connect('switched', self.on_view_switched)
        # sw.view = main_model.view
        # main_model.bind_property('view', sw, 'view', 1)
        box.pack_start(sw, False, False, 0)

        box = Gtk.Box.new(orientation=1, spacing=0)

        search_bar = Gtk.SearchBar()
        searchentry = Gtk.SearchEntry()
        search_bar.add(searchentry)
        search_bar.connect_entry(searchentry)
        # search_bar.set_search_mode(True)
        box.pack_start(search_bar, False, True, 0)



        # VIEW SWITCHER

        # set_combo = Gtk.ComboBoxText()
        # set_combo.append_text('dksdk test')
        # hbox.pack_start(set_combo, False, False, 0)
        self.add(box)

        self.notebook = Notebook()


        box.pack_start(self.notebook, True, True, 0)

        screen = Gdk.Screen.get_default()
        # css_provider = Gtk.CssProvider.get_named('Adwaita', 'dark')
        css_provider_file = Gtk.CssProvider()
        css_provider_file.load_from_path(CONFIG['css'])
        context = Gtk.StyleContext()
        # # context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        context.add_provider_for_screen(screen, css_provider_file, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.show_all()
        main_model.view = 'listview'
        self.init_sets()
        self.set_icon_from_file(CONFIG['icon'])
        # alias_entry.grab_focus()

        adv = AliasesDirView()
        adv.connect('file-list', self.on_file_list)
        adv.connect('tag-edit', self.on_tag_edit)
        num = self.notebook.append_buttom(adv,'Search')
        self.notebook.set_current_page(num)

    def on_sstack_key_pressed(self, widget, event, science):
        science.popup()
        science.file_search.grab_focus()
        science.file_search.set_text(event.string)
        science.file_search.set_position(-1)

    def on_group_combo_changed(self, widget):
        tree_iter = widget.get_active_iter()
        if tree_iter is not None:
            model = widget.get_model()
            country = model[tree_iter][0]
            print("Selected: country=%s" % country)

    def on_menu_tags_details_activated(self, widget):
        det_store.clear()
        qu = Query.get_tag_details('archives')
        for q in qu:
            det_store.append(q)
        self.stack.set_visible_child_full('detail', 0)

    # def on_model_col_changed(self, obj, col_int):
    #     tag_store.clear()
    #     tag_icon_store.clear()
    #     # for q in Query.get_tags(col_int):
    #     #     tag_store.append(q)
    #     for q in Query.get_tags(col_int):
    #         tag_store.append(q)
    #         try:
    #             pb = Pixbuf.new_from_file_at_size(f'/media/soni/1001/persistent/1001/thumbs/{q[3]}.jpg', 192, 192)
    #             # pb = Pixbuf.new_from_file(f'/media/soni/1001/persistent/1001/avatars/{q[0]}.jpg')
    #         except GLib.Error:
    #             # avatar = Pixbuf.new_from_file_at_size('/usr/share/icons/Adwaita/256x256/status/avatar-default.png', 192, 192)
    #             pb = avatar
    #         tag_icon_store.append((q[0], q[1], pb,))
    #     self.stack.set_visible_child_full('icontag', 0)


    # def on_model_view_changed(self, obj, stack):
    #     if obj.query_type < QueryType.TAGREAD:
    #         stack.set_visible_child_full('files', 0)
    #     else:
    #         if obj.query_type == QueryType.TAGREAD:pass
    #         elif obj.query_type == QueryType.TAGUPDATE:
    #             stack.set_visible_child_full('tagedit', 0)
    #         elif obj.query_type == QueryType.FILEUPDATE:
    #             stack.set_visible_child_full('fileedit', 0)


    def on_view_switched(self, widget):
        num = self.notebook.get_current_page()
        child = self.notebook.get_nth_page(num)
        child.set_view(widget.view)

    def on_tag_edit_list_tag(self, widget, tag_id):
        # main_model.set_type(QueryType.TAG, tag_id, None)
        # selection = widget.get_selection()
        # model, iter = selection.get_selected()
        tag_edit = TagEdit()
        # tag_edit.connect('list-tag', self.on_tag_edit_list_tag)
        num = self.notebook.append_buttom(tag_edit, 'edit')
        self.notebook.set_current_page(num)


    def on_icon_tag_item_activated(self, widget, path):
        model = widget.get_model()
        iter = model.get_iter(path[0])
        main_model.set_type(QueryType.TAGUPDATE, model[iter][0], None)

    def on_menu_move_and_vindex_activated(self, widget):
        shell_commands.movetotemp()

    def on_tag_filenames(self, widget, tag_id, clipboard):
        res = Query.get_tag_column(tag_id)
        clipboard.set_text(res, -1)

    def on_science_filename_filter_changed(self, widget, text):
        main_model.set_filter(f'%{text}%')

    def on_science_sort_changed(self, widget, text):
        sort_text, order_text = text.split(',')
        main_model.set_sort_and_order(sort_text, order_text)

    def on_page_changed(self, widget):
        main_model.set_page(widget.get_value())

    def on_menu_all_files_activated(self, widget):
        main_model.set_type(QueryType.TAGALL, -1, None)

    def on_menu_untagged_files_activated(self, widget):
        main_model.set_type(QueryType.TAG0, -1, None)

    def on_menu_onetag_files_activated(self, widget):
        main_model.set_type(QueryType.TAG1, -1, None)

    # def on_menu_nocol_tags_activated(self, widget):
    #     tag_store.clear()
    #     for q in Query.get_tags():
    #         tag_store.append(q)

    def on_view_notified(self, obj, gparamstring, stack):
        stack.set_visible_child_full(obj.view, 0)

    def on_file_edit(self, widget, file_id, alias):
        f_edit = FileEdit(file_id, alias)
        f_edit.show_all()
        # tag_edit.connect('list-tag', self.on_tag_edit_list_tag)
        num = self.notebook.append_buttom(f_edit,'📝\t'+ alias)
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
   
    def on_tag_read_smart(self, widget, *args):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        main_model.set_type(QueryType.TAG, model[iter][0], None)
        
    def on_tag_read(self, widget, *args):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        self.on_file_list(widget, model[iter][0], model[iter][1])

    def on_file_list(self, widget, tag_id, tag_name):
        fw = FileView(tag_id, tag_name)
        fw.connect('file-edit', self.on_file_edit)
        num = self.notebook.append_buttom(fw, '🔍\t'+tag_name)
        self.notebook.set_current_page(num)

    def on_tag_edit(self, widget, tag_id, tag_name):
        # selection = widget.get_selection()
        # model, iter = selection.get_selected()
        tag_edit = TagEdit(tag_id, tag_name)
        tag_edit.show_all()
        tag_edit.connect('file-list', self.on_file_list)
        num = self.notebook.append_buttom(tag_edit, '🔖\t'+ tag_name)
        self.notebook.set_current_page(num)

    def init_sets(self):
        # for q in Query.get_cols():
        #     col_store.append(q)
        col_store.init(Query.get_tree())

        # for q in Query.get_tags(-1):
        #     tag_store.append(q)

    def on_window_delete_event(self, widget, event):
        Gtk.main_quit()