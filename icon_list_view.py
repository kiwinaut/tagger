from gi.repository import Gtk, GObject, Gdk
from gi.repository.GdkPixbuf import Pixbuf
from print_pretty.pretty_size import psize
# from enums import Mime, StoreMainPosition

# from gi.repository import GdkPixbuf
# from settings import App
# from menus import IconMenu
# from dialogs import EditDialog
# import windows
# import popovers
# from cell_functions import *
# from math import pi
# from resources import band_pixbuf, nonepix
# import row_proxy
# import tools
# from profiling import timethis

# t_pixbuf = GdkPixbuf.Pixbuf.new_from_file('data/emblem-generic.png')
# bit_pixbuf = GdkPixbuf.Pixbuf.new_from_file('data/bit.png')
# band_pixbuf = GdkPixbuf.Pixbuf.new_from_file('data/band.png')
def ctime_cell_data_func(tree_column, cell, tree_model, iter, data):
    date = tree_model[iter][4]
    cell.set_property('text', date.strftime('%d %b %y'))

def size_cell_data_func(tree_column, cell, tree_model, iter, data):
    date = tree_model[iter][3]
    cell.set_property('text', psize(date))


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

            

class ListView(Gtk.TreeView):
    __gsignals__ = {
      'file-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
      # 'edit': (GObject.SIGNAL_RUN_FIRST, None, (object, object,)),
    }
    def __init__(self, accel=None):
        Gtk.TreeView.__init__(self, has_tooltip=True)
        # self.set_property('headers-visible', True)
        self.set_rules_hint(True)
        self.get_selection().set_mode(3)
        self.set_rubber_banding(True)
        self.set_search_column(2)
        # entry = self.get_search_entry()
        self.set_enable_search(False)

        # self.connect('query-tooltip', self.on_tooltip_queried)

        self.accel = accel


        # column = Gtk.TreeViewColumn('Thumb')
        # self.thumb_column = column
        # renderer = Gtk.CellRendererPixbuf()
        # column.pack_start(renderer, False)
        # # renderer.set_alignment(0.5, 0.5)
        # # column.add_attribute(renderer,'pixbuf',StoreMainPosition.THUMB)
        # column.set_cell_data_func(renderer,ListPixbufCellLayoutDataFunc,None)
        # self.thumb_column = column
        # self.append_column(column)

        #1
        column = Gtk.TreeViewColumn(title='Set')
        # column.position = StoreMainPosition.SET
        column.set_resizable(True)
        # self.set_col = column
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','Ubuntu 10')
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 5)
        # column.set_sort_column_id(StoreMainPosition.SET)
        self.append_column(column)

        # column = Gtk.TreeViewColumn(title='Filename')
        # column.set_resizable(True)
        # # column.position = StoreMainPosition.NAME
        # # self.name_col = column
        # renderer = Gtk.CellRendererText()
        # renderer.set_property('font','Ubuntu 10')
        # column.pack_start(renderer, True)
        # column.add_attribute(renderer, 'text', 2)
        # # column.set_sort_column_id(StoreMainPosition.NAME)
        # self.append_column(column)


        # column = Gtk.TreeViewColumn('Group')
        # column.set_resizable(True)
        # column.position = StoreMainPosition.GROUP
        # self.group_col = column
        # renderer = Gtk.CellRendererText()
        # renderer.set_property('font','Ubuntu 10')
        # renderer.set_property('ellipsize',3)
        # column.pack_start(renderer, True)
        # column.add_attribute(renderer, 'text', StoreMainPosition.GROUP)
        # # column.set_sort_column_id(StoreMainPosition.GROUP)
        # self.append_column(column)

        # column = Gtk.TreeViewColumn('Tag')
        # column.set_resizable(True)
        # column.position = StoreMainPosition.TAG
        # self.tag_col = column
        # renderer = Gtk.CellRendererText()
        # renderer.set_property('font','Ubuntu 10')
        # renderer.set_property('ellipsize',3)
        # column.pack_start(renderer, True)
        # column.add_attribute(renderer, 'text', StoreMainPosition.TAG)
        # # column.set_sort_column_id(StoreMainPosition.GROUP)
        # self.append_column(column)

        column = Gtk.TreeViewColumn('Mtime')
        column.set_clickable(True)
        # column.position = StoreMainPosition.MTIME
        # self.ctime_col = column
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        column.pack_start(renderer, True)

        # column.add_attribute(renderer, 'text', 7)
        column.set_cell_data_func(renderer, ctime_cell_data_func, func_data=None)
        # column.set_sort_column_id(4)        
        self.append_column(column)

        column = Gtk.TreeViewColumn('Size')
        # column.position = StoreMainPosition.SIZE
        # self.size_col = column
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        column.pack_start(renderer, True)
        # column.add_attribute(renderer, 'text', 8)
        # column.set_sort_column_id(StoreMainPosition.SIZE)
        column.set_cell_data_func(renderer, size_cell_data_func, func_data=None)        
        self.append_column(column)

        column = Gtk.TreeViewColumn('Count')
        # column.position = StoreMainPosition.COUNT
        # self.count_col = column
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        # renderer.set_property('alignment', 1)
        # column.set_cell_data_func(renderer, count_cell_data_func, func_data=None)
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 7)
        # column.set_sort_column_id(StoreMainPosition.COUNT)
        # column.set_fixed_width(50)
        # column.set_sort_indicator(True)
        # column.set_clickable(True)
        self.append_column(column)

        column = Gtk.TreeViewColumn('Note')
        # column.position = StoreMainPosition.NOTE
        # self.note_col = column
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        renderer.set_property('ellipsize',3)
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 6)
        # column.set_sort_column_id(StoreMainPosition.NOTE)
        self.append_column(column)

        column = Gtk.TreeViewColumn('Filename')
        # column.position = StoreMainPosition.FILENAME
        # self.filename_col = column
        renderer = Gtk.CellRendererText()
        renderer.set_property('font','10')
        renderer.set_property('foreground','grey')
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 2)
        # column.set_cell_data_func(renderer, file_cell_data_func, func_data=None)        
        # column.set_sort_column_id(1)
        self.append_column(column)

        # self.thumb_view = popovers.ThumbPopOver(self)
        # self.rename_popover = popovers.RenamePopOver(self)
        # self.renote_popover = popovers.UpdatePopOver(self)
        # self.reset_popover = popovers.UpdatePopOver(self)
        # self.regroup_popover = popovers.RegroupPopOver(self)
        # self.renote_popover.connect('update',self.on_popover_updated, StoreMainPosition.NOTE)
        # self.reset_popover.connect('update',self.on_popover_updated, StoreMainPosition.SET)
        # self.rename_popover.connect('update',self.on_popover_updated, StoreMainPosition.NAME)
        # self.regroup_popover.connect('update',self.on_popover_updated, StoreMainPosition.GROUP)

        menu = Gtk.Menu()
        read = Gtk.MenuItem.new_with_label('Read')
        # read.connect('activate', self.on_menu_read_activate)
        menu.append(read)
        update = Gtk.MenuItem.new_with_label('Update')
        # update.connect('activate', self.on_menu_update_activate)
        menu.append(update)
        menu.show_all()

        # self.connect('row-activated', self.on_menu_read_activate)

        menu = Gtk.Menu()
        read = Gtk.MenuItem.new_with_label('Read')
        read.connect('activate', self.on_menu_read_activate)
        menu.append(read)
        # update = Gtk.MenuItem.new_with_label('Update')
        # update.connect('activate', self.on_menu_update_activate)
        # menu.append(update)
        menu.show_all()
        # self.dirmenu = menu
        # self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect('button-press-event', self.show_menu, menu)

        self.connect('row-activated', self.on_menu_read_activate)

        # self.icon_menu = IconMenu()
        # self.icon_menu.open_file.connect('activate', self.on_menu_open_file_activated)
        # self.icon_menu.open_loc.connect('activate', self.on_menu_open_loc_activated)
        # self.icon_menu.reload.connect('activate', self.on_menu_reload_activated)
        # self.icon_menu.rethumb.connect('activate', self.on_menu_rethumb_activated)
        # self.icon_menu.edit.connect('activate', self.on_menu_edit_activated)
        # self.icon_menu.edit.add_accelerator("activate",
        #                                    self.accel,
        #                                    Gdk.keyval_from_name("e"),
        #                                    Gdk.ModifierType.CONTROL_MASK,
        #                                    Gtk.AccelFlags.VISIBLE)
        # self.icon_menu.del_entry.connect('activate', self.on_menu_del_entry_activated)
        # self.icon_menu.del_both.connect('activate', self.on_menu_del_both_activated)
        # self.show_all()
    def build_menu(self):
        self.menu = Gtk.Menu()
        copy = Gtk.MenuItem('Copy')
        # copy.connect('activate', self.copy)
        paste = Gtk.MenuItem('Paste')
        # paste.connect('activate', self.paste)
        self.menu.append(copy)
        self.menu.append(paste)

    def show_menu(self, widget, event, menu):
        """show_menu
        Shows the right click menu of the current item.
        """
        button = event.button
        if button == Gdk.BUTTON_SECONDARY:
            menu.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        return None

    def on_menu_read_activate(self, widget, *args):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)
        self.emit('file-update', model[iter][0])
        # model.remove(iter)

    def on_tooltip_queried(self, widget, x, y, keyboard_mode, tooltip):
        values = self.get_path_at_pos(x,y-24)
        if values:
            path, column, cell_x, cell_y = values
            if column.position == StoreMainPosition.THUMB:
                model = self.get_model()
                iter = model.get_iter(path)
                pix = model[iter][StoreMainPosition.THUMB]
                tooltip.set_icon(pix)
                return True

    def on_menu_open_file_activated(self, widget):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()

        iter = model.get_iter(paths[0])
        row = row_proxy.RowTree(model, iter)
        row.open_file()

    def on_menu_open_loc_activated(self, widget):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()

        iter = model.get_iter(paths[0])
        row = row_proxy.RowTree(model, iter)
        row.open_folder()

    def on_menu_reload_activated(self, widget):pass
    def on_menu_rethumb_activated(self, widget):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        iter = model.get_iter(paths[0])
        self.emit('rethumb', model, iter)

    def on_menu_edit_activated(self, widget):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        if not len(paths) >= 2:
            iter = model.get_iter(paths[0])
            window = windows.EditWindow(self.get_toplevel())
            row = row_proxy.RowTree(model, iter)
            window.set_row(row)
        else:
            window = windows.EditWindowMultiple(self.get_toplevel())
            row = row_proxy.RowTreeMultiple(model, paths)
            window.set_row(row)

    def on_get_screenshot(self, widget, model, iter):
        row = row_proxy.RowTree(model, iter)
        pixbuf = row.get_screenshot()
        w = windows.ScreenShotWindow(self.get_toplevel(), pixbuf)
        w.show_all()
        print(self.get_toplevel())

    def on_menu_del_entry_activated(self, widget):pass
    def on_menu_del_both_activated(self, widget):pass

    def on_popover_updated(self, widget, value, model, iter, pos):
        if pos == StoreMainPosition.NAME:
            model[iter][StoreMainPosition.NAME] = value
            #TODO query
        elif pos == StoreMainPosition.GROUP:
            model[iter][StoreMainPosition.GROUP] = value
            #TODO query
        elif pos == StoreMainPosition.SET:
            model[iter][StoreMainPosition.SET] = value
                #TODO query
        elif pos == StoreMainPosition.NOTE:
            model[iter][StoreMainPosition.NOTE] = value
                    #TODO query
                    
    def on_row_activated(self, tree_view, path, column):
        if column == self.name_col:
            popover = self.rename_popover
            position = StoreMainPosition.NAME
        elif column == self.group_col:
            popover = self.regroup_popover
            position = StoreMainPosition.GROUP
        elif column == self.thumb_column:
            model = tree_view.get_model()
            iter = model.get_iter(path)
            value = model[iter][StoreMainPosition.THUMB]
            self.on_get_screenshot(tree_view, model, iter)
            return
            # popover = self.thumb_view
            # position = StoreMainPosition.THUMB
        elif column == self.note_col:
            popover = self.renote_popover
            position = StoreMainPosition.NOTE
        elif column == self.set_col:
            popover = self.reset_popover
            position = StoreMainPosition.SET
        elif column == self.filename_col:
            model = tree_view.get_model()
            iter = model.get_iter(path)
            row = row_proxy.RowTree(model, iter)
            row.openfile()
            return


        rect = self.get_background_area(path, column)
        rect.y = rect.y + 8
        model = tree_view.get_model()
        iter = model.get_iter(path)
        value = model[iter][position]
        popover.set_pointing_to(rect)
        if position == StoreMainPosition.THUMB:
            popover.set_image(value)
        else:
            popover.set_text(value)
            popover.set_model_iter(model, iter)
            button = popover.get_default_widget()
            button.grab_default()
        popover.popup()


    # def do_button_press_event(self, event):
    #     if event.button == Gdk.BUTTON_SECONDARY:
    #         selection = self.get_selection()
    #         pos = self.get_path_at_pos(event.x, event.y)# path, column, cell_x, cell_y
    #         if pos:
    #             #clicked any content
    #             path, column, cell_x, cell_y = pos
    #             if selection.path_is_selected(path):
    #                 #clicked in selection
    #                 self.dirmenu.popup(None, None, None, None, event.button, event.time)
    #             else:
    #                 #clicked outside of selection
    #                 Gtk.TreeView.do_button_press_event(self, event)
    #                 self.dirmenu.popup(None, None, None, None, event.button, event.time)
    #         else:
    #             #clicked empty area
    #             selection.unselect_all()
    #             return False
    #     else:
    #         Gtk.TreeView.do_button_press_event(self, event)


class IconView(Gtk.IconView):
    __gsignals__ = {
      'rethumb': (GObject.SIGNAL_RUN_FIRST, None, (object, object,)),
      'edit': (GObject.SIGNAL_RUN_FIRST, None, (object, object,)),
    }
    def __init__(self, accel):
        Gtk.IconView.__init__(self, has_tooltip=True)
        self.set_item_width(0)
        self.set_property('margin',2)
        self.set_row_spacing(0)
        self.set_column_spacing(0)
        self.set_item_padding(2)
        self.accel = accel

        self.connect('query-tooltip', self.on_tooltip_queried)

        # renderer = Gtk.CellRendererPixbuf()
        renderer = CustomRendererPixbuf()
        self.pack_start(renderer, False)
        renderer.set_alignment(0.5, 0.5)
        self.thumb_renderer = renderer
        self.add_attribute(renderer,'pixbuf',StoreMainPosition.THUMB_128)
        self.add_attribute(renderer,'mime',StoreMainPosition.MIME)
       # self.set_cell_data_func(renderer,PixbufCellLayoutDataFunc,None)

        srenderer = Gtk.CellRendererText()
        self.pack_start(srenderer, False)
        srenderer.set_property('font','Ubuntu 9')
        srenderer.set_property('ellipsize', 2)
        srenderer.set_alignment(0.5, 0.5)
        srenderer.set_property('max-width-chars', 10)
        self.add_attribute(srenderer,'text',StoreMainPosition.SET)
        
        trenderer = Gtk.CellRendererText()
        self.pack_start(trenderer, False)
        self.add_attribute(trenderer,'text',StoreMainPosition.FILENAME)
        # self.set_cell_data_func(trenderer,FileCellLayoutDataFunc,None)
        trenderer.set_property('font','Ubuntu 9')
        trenderer.set_alignment(0.5, 0.5)
        trenderer.set_property('foreground','grey')
        trenderer.set_property('ellipsize', 2)
        trenderer.set_property('max-width-chars', 10)

        self.icon_menu = IconMenu()
        self.icon_menu.open_file.connect('activate', self.on_menu_open_file_activated)
        self.icon_menu.open_loc.connect('activate', self.on_menu_open_loc_activated)
        self.icon_menu.reload.connect('activate', self.on_menu_reload_activated)
        self.icon_menu.rethumb.connect('activate', self.on_menu_rethumb_activated)
        self.icon_menu.edit.connect('activate', self.on_menu_edit_activated)
        self.icon_menu.edit.add_accelerator("activate",
                                           self.accel,
                                           Gdk.keyval_from_name("e"),
                                           Gdk.ModifierType.CONTROL_MASK,
                                           Gtk.AccelFlags.VISIBLE)
        self.icon_menu.del_entry.connect('activate', self.on_menu_del_entry_activated)
        self.icon_menu.del_both.connect('activate', self.on_menu_del_both_activated)

    def on_tooltip_queried(self, widget, x, y, keyboard_mode, tooltip):
        treepath = self.get_path_at_pos(x,y)
        if treepath:
            model = self.get_model()
            iter = model.get_iter(treepath)
            pix = model[iter][StoreMainPosition.THUMB]
            tooltip.set_icon(pix)
            return True

    def set_thumb_cell_position(self, position):
        self.clear_attributes(self.thumb_renderer)
        self.add_attribute(self.thumb_renderer,'pixbuf',position)
        self.add_attribute(self.thumb_renderer,'mime',StoreMainPosition.MIME)
        self.emit('size-allocate', self.get_allocation())

    def on_menu_open_file_activated(self, widget):pass
    def on_menu_open_loc_activated(self, widget):pass
    def on_menu_reload_activated(self, widget):pass


    def on_menu_rethumb_activated(self, widget):
        paths = self.get_selected_items()
        model = self.get_model()
        iter = model.get_iter(paths[0])
        self.emit('rethumb', model, iter)


    def on_menu_edit_activated(self, widget):
        paths = self.get_selected_items()
        model = self.get_model()
        if not len(paths) >= 2:
            iter = model.get_iter(paths[0])
            window = windows.EditWindow(self.get_toplevel(), model)
            window.set_row(iter)

    def on_menu_del_entry_activated(self, widget):pass
    def on_menu_del_both_activated(self, widget):pass



    def do_button_press_event(self, event):
        if event.button == Gdk.BUTTON_SECONDARY:
            selection = self.get_selected_items()
            path = self.get_path_at_pos(event.x, event.y)
            # selection = self.get_selection()
            # pos = self.get_path_at_pos(event.x, event.y)# path, column, cell_x, cell_y
            if path:
                #clicked any content
                if path in selection:
                    #clicked in selection
                    self.icon_menu.popup(None, None, None, None, event.button, event.time)
                else:
                    #clicked outside of selection
                    # Gtk.IconView.do_button_press_event(self, event)
                    self.unselect_all()
                    self.select_path(path)

                    self.icon_menu.popup(None, None, None, None, event.button, event.time)
            else:
                #clicked empty area
                self.unselect_all()
                return False
        else:
            Gtk.IconView.do_button_press_event(self, event)



# class IconListView(Gtk.Box):
#     # __gsignals__ = {
#     #     'view-search': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
#     #     'search': (GObject.SIGNAL_RUN_FIRST, None, (object,object,object,)),
#     #     'delete': (GObject.SIGNAL_RUN_FIRST, None, (object, str,)),
#     #     'update': (GObject.SIGNAL_RUN_FIRST, None, (object, object, str,)),
#     # }
#     def __init__(self, accel):
#         Gtk.Box.__init__(self, orientation = 1 ,spacing=0)

#         hbox = Gtk.Box.new(orientation = 0 ,spacing=4)
#         hbox.set_property('margin', 4)
#         # hbox.set_shadow_type(1)

#         switcher = ViewSwitcher()

#         hbox2 = Gtk.Box.new(orientation = 0 ,spacing=0)
#         hbox2.get_style_context().add_class("linked")

#         togg1 = Gtk.ToggleButton()
#         togg1.set_property('active', App.FILTER_LIBIMAGE)
#         img = Gtk.Image.new_from_icon_name('image-x-generic', 2)
#         togg1.set_image(img)
#         self.libimage = togg1
#         hbox2.pack_start(togg1, False, False, 0)

#         togg2 = Gtk.ToggleButton()
#         togg2.set_property('active', App.FILTER_ARCHIVE)
#         img = Gtk.Image.new_from_icon_name('package-x-generic', 2)
#         togg2.set_image(img)
#         self.archive = togg2
#         hbox2.pack_start(togg2, False, False, 0)

#         togg3 = Gtk.ToggleButton()
#         togg3.set_property('active', App.FILTER_VIDEO)
#         img = Gtk.Image.new_from_icon_name('video-x-generic', 2)
#         togg3.set_image(img)
#         self.video = togg3
#         hbox2.pack_start(togg3, False, False, 0)


#         hbox.pack_end(hbox2, False, False, 0)

#         label = Gtk.Label('Name Group')
#         hbox.pack_end(label, True, True, 0)

#         #<>
#         box = Gtk.Box(0,0)
#         box.get_style_context().add_class("linked")

#         self.previous = Gtk.Button()
#         img = Gtk.Image.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.MENU)
#         self.previous.set_image(img)
#         # self.previous.set_sensitive(False)
#         box.pack_start(self.previous, False, True, 0)

#         self.next = Gtk.Button()
#         img = Gtk.Image.new_from_icon_name("go-next-symbolic", Gtk.IconSize.MENU)
#         self.next.set_image(img)
#         # self.next.set_sensitive(False)
#         box.pack_start(self.next, False, True, 0)

#         hbox.pack_end(box, False, True, 0)

#         hbox.pack_end(switcher, False, False, 0)



#         self.pack_start(hbox, False, False, 0)

#         self.stack = Gtk.Stack()
#         self.pack_end(self.stack, True, True, 0)
#         switcher.set_stack(self.stack)

#         sc_icon = Gtk.ScrolledWindow()
#         self.sc1 = sc_icon
#         icon = IconView()

#         self.icon =icon
#         sc_icon.add(icon)
#         sc_icon.show_all()
#         self.stack.add_titled(sc_icon, 'icon', 'icon')


#         sc_list = Gtk.ScrolledWindow()
#         self.sc2 = sc_list
#         tree = ListView(accel=accel)
#         self.list = tree
#         ##############################

#         ####################
#         sc_list.add(tree)
#         sc_list.show_all()
#         self.stack.add_titled(sc_list, 'list', 'list')
#         self.stack.set_visible_child(sc_list)




#         self.show_all()

#     def set_model(self, model):
#         self.icon.set_model(model)
#         self.list.set_model(model)





