from gi.repository import Gtk, Gdk, GObject, GLib
from models import Query
from humanfriendly import format_size
# from shell_commands import open_file, trash_file
# from clip import rethumb
# from data_models import  main_model
# from humanfriendly import format_size
# from stores import folder

def size_cell_data_func(tree_column, cell, tree_model, iter, data):
    cell.set_property('text', format_size(tree_model[iter][2]))

target2 = Gtk.TargetEntry.new('FOLDER', Gtk.TargetFlags.SAME_WIDGET, 1)
target3 = Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags.SAME_APP, 0)
target4 = Gtk.TargetEntry.new('TAG', Gtk.TargetFlags.SAME_APP, 0)


class MainSignals(GObject.GObject):
    __gsignals__ = {
        'file-update': (GObject.SIGNAL_RUN_FIRST, None, (int, str,)),
    }
    def __init__(self):
        GObject.GObject.__init__(self)


class TabViewBase(Gtk.Box):
    view = GObject.Property(type=str, default="gridview")
    scale = GObject.Property(type=float, default=8.0)
    __gsignals__ = {
        'file-edit': (GObject.SIGNAL_RUN_FIRST, None, (int,str,)),
        'tag-edit': (GObject.SIGNAL_RUN_FIRST, None, (int,str,)),
        'file-list': (GObject.SIGNAL_RUN_FIRST, None, (int,str,)),
    }
    def __init__(self, *args, **kw):
        Gtk.Box.__init__(self, *args, **kw)

    def get_view(self):
        raise Exception

    def set_view(self, value):pass

    def get_scale(self):
        raise Exception

    def set_scale(self, value):pass


class ThumbTile(Gtk.Overlay):
    def __init__(self, set, path, pix):
        Gtk.Overlay.__init__(self, name='ThumbTile')
        self.get_style_context().add_class("thumbtile")
        grid = Gtk.Grid()
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        set = Gtk.Label(set)
        path = Gtk.Label(path)
        img = Gtk.Image.new_from_pixbuf(pix)
        img.set_vexpand(True)
        grid.attach(img, 0,0,1,1)
        grid.attach(set, 0,1,1,1)
        grid.attach(path, 0,2,1,1)

        self.add(grid)


class QuestionDialog(Gtk.MessageDialog):
    def __init__(self, widget, msg):
        Gtk.MessageDialog.__init__(self, 
            widget.get_toplevel(), 
            0, 
            Gtk.MessageType.QUESTION,
            Gtk.ButtonsType.YES_NO,
            f"Are You Sure?"
            )
        self.format_secondary_text(msg)

class DetailView(Gtk.TreeView):
    __gsignals__ = {
        'tag-read': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'tag-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'tag-delete': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'filenames': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    }
    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.set_enable_search(False)
        # self.set_property('headers-visible', False)

        column = Gtk.TreeViewColumn('alias')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 0)
        column.set_sort_column_id(0)
        self.append_column(column)

        column = Gtk.TreeViewColumn('count')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 1)
        column.set_sort_column_id(1)
        self.append_column(column)

        column = Gtk.TreeViewColumn('size')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        # column.add_attribute(renderer, 'text', 2)
        column.set_cell_data_func(renderer, size_cell_data_func, func_data=None)
        column.set_sort_column_id(2)
        self.append_column(column)

        # menu = Gtk.Menu()
        # delete = Gtk.MenuItem.new_with_label('Delete')
        # delete.connect('activate', self.on_menu_delete_activate)
        # menu.append(delete)
        # delete = Gtk.MenuItem.new_with_label('Read')
        # delete.connect('activate', self.on_menu_read_activate)
        # menu.append(delete)
        # delete = Gtk.MenuItem.new_with_label('Update')
        # delete.connect('activate', self.on_menu_update_activate)
        # menu.append(delete)

        # delete = Gtk.MenuItem.new_with_label('Filenames')
        # delete.connect('activate', self.on_menu_filenames_activate)
        # menu.append(delete)

        # menu.show_all()
        # # self.connect('row-activated', self.on_menu_read_activate)
        # self.dirmenu = menu


# class TagView(Gtk.TreeView):
#     __gsignals__ = {
#         'tag-read': (GObject.SIGNAL_RUN_FIRST, None, ()),
#         'tag-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
#         'tag-delete': (GObject.SIGNAL_RUN_FIRST, None, ()),
#         'filenames': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
#     }
#     def __init__(self):
#         Gtk.TreeView.__init__(self)
#         self.set_enable_search(False)
#         self.set_property('headers-visible', False)

#         column = Gtk.TreeViewColumn('name')

#         alias = Gtk.CellRendererText()
#         column.pack_start(alias, True)
#         column.add_attribute(alias, 'text', 1)

#         # renderer = Gtk.CellRendererText()
#         # column.pack_start(renderer, False)
#         # column.add_attribute(renderer, 'text', 2)
#         self.append_column(column)

#         menu = Gtk.Menu()
#         delete = Gtk.MenuItem.new_with_label('Delete')
#         delete.connect('activate', self.on_menu_delete_activate)
#         menu.append(delete)
#         delete = Gtk.MenuItem.new_with_label('Read')
#         delete.connect('activate', self.on_menu_read_activate)
#         menu.append(delete)
#         delete = Gtk.MenuItem.new_with_label('Update')
#         delete.connect('activate', self.on_menu_update_activate)
#         menu.append(delete)

#         delete = Gtk.MenuItem.new_with_label('Filenames')
#         delete.connect('activate', self.on_menu_filenames_activate)
#         menu.append(delete)

#         menu.show_all()
#         # self.connect('row-activated', self.on_menu_read_activate)
#         self.dirmenu = menu

#         self.enable_model_drag_source(
#             Gdk.ModifierType.BUTTON1_MASK|Gdk.ModifierType.CONTROL_MASK,
#             [target3, target4],
#             Gdk.DragAction.COPY
#         )
#         self.connect("drag-data-get", self.on_drag_data_get)

#     def on_drag_data_get(self, widget, drag_context, data, info, time):
#         selection = widget.get_selection()
#         model, iter = selection.get_selected()
#         # path = model.get_path(iter)
#         # value = '{}\n{}'.format(*model.get(iter, 0, 1))
#         # value = path.to_string()
#         if str(data.get_target()) == 'TAG':
#             value = str(model[iter][0])
#             data.set(data.get_target(), 8, bytes(value, "utf-8"))
#         elif str(data.get_target()) == 'text/plain':
#             string = model[iter][1]
#             data.set(data.get_target(), 8, bytes(string, "utf-8"))


#     def on_menu_filenames_activate(self, widget, *args):
#         selection = self.get_selection()
#         model, iter = selection.get_selected()
#         # self.emit('tag-read', model[iter][0], model[iter][1])
#         self.emit('filenames', model[iter][0])

#     def on_menu_read_activate(self, widget, *args):
#         # selection = self.get_selection()
#         # model, iter = selection.get_selected()
#         # self.emit('tag-read', model[iter][0], model[iter][1])
#         self.emit('tag-read')

#     def on_menu_update_activate(self, widget, *args):
#         # selection = self.get_selection()
#         # model, iter = selection.get_selected()
#         # self.emit('tag-update', model[iter][0], model[iter][1])

#         self.emit('tag-update')#tag_id
#         # somewhere updated
#         # update model in here or there?

#     def on_menu_delete_activate(self, widget, *args):
#         # sure
#         # db del
#         # self del

#         # selection = self.get_selection()
#         # model, iter = selection.get_selected()
#         # self.emit('tag-delete', model[iter][0], model[iter][1])
#         self.emit('tag-delete')

#     def do_button_press_event(self, event):
#         if event.button == Gdk.BUTTON_SECONDARY:
#             selection = self.get_selection()
#             pos = self.get_path_at_pos(event.x, event.y)# path, column, cell_x, cell_y
#             if pos:
#                 #clicked any content
#                 path, column, cell_x, cell_y = pos
#                 if selection.path_is_selected(path):
#                     #clicked in selection
#                     self.dirmenu.popup(None, None, None, None, event.button, event.time)
#                 else:
#                     #clicked outside of selection
#                     Gtk.TreeView.do_button_press_event(self, event)
#                     self.dirmenu.popup(None, None, None, None, event.button, event.time)
#             else:
#                 #clicked empty area
#                 selection.unselect_all()
#                 return False
#         else:
#             Gtk.TreeView.do_button_press_event(self, event)

def TreeCellDataFunc(tree_column, cell, tree_model, iter, data):
    if cell.get_property('is-expanded'):
        cell.set_property('icon-name', 'folder-drag-accept')
    # elif cell.get_property('is-expander'):
    #     cell.set_property('icon-name', 'folder')
    else:
        cell.set_property('icon-name', 'folder')

class DialogExample(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Entry Dialog", parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OK, Gtk.ResponseType.OK))

        self.set_default_size(150, 100)

        entry = Gtk.Entry()
        self.entry = entry

        box = self.get_content_area()
        box.add(entry)
        self.show_all()

class TagTreeView(Gtk.TreeView):
    __gsignals__ = {
        'tag-read': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'tag-update': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'tag-delete': (GObject.SIGNAL_RUN_FIRST, None, ()),
        'filenames': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    }
    def __init__(self):
        Gtk.TreeView.__init__(self)
        self.set_property('headers-visible', False)
        self.set_enable_tree_lines(True)
        self.set_enable_search(False)
        # self.set_grid_lines(1)
        # self.set_show_expanders(True)

        column = Gtk.TreeViewColumn('name')
        
        renderer = Gtk.CellRendererPixbuf()
        renderer.set_property('icon-name', 'folder-visiting-symbolic')
        renderer.set_property('xpad', 2)
        # column.set_cell_data_func(renderer, TreeCellDataFunc, None)
        column.pack_start(renderer, False)

        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 2)
        self.append_column(column)


        menu = Gtk.Menu()
        delete = Gtk.MenuItem.new_with_label('New')
        delete.connect('activate', self.on_menu_new_activate)
        menu.append(delete)
        delete = Gtk.MenuItem.new_with_label('Show Tags')
        delete.connect('activate', self.on_menu_read_activate)
        menu.append(delete)
        delete = Gtk.MenuItem.new_with_label('Update')
        delete.connect('activate', self.on_menu_update_activate)
        menu.append(delete)
        delete = Gtk.MenuItem.new_with_label('Delete')
        delete.connect('activate', self.on_menu_delete_activate)
        menu.append(delete)

        delete = Gtk.MenuItem.new_with_label('Filenames')
        delete.connect('activate', self.on_menu_filenames_activate)
        self.connect('key-press-event', self.on_key_pressed)

        menu.append(delete)

        menu.show_all()
        # self.connect('row-activated', self.on_menu_read_activate)
        self.dirmenu = menu


        self.enable_model_drag_source(
            Gdk.ModifierType.BUTTON1_MASK|Gdk.ModifierType.CONTROL_MASK,
            [target2, target3],
            Gdk.DragAction.COPY|Gdk.DragAction.MOVE
        )
        self.connect("drag-data-get", self.on_drag_data_get)
        self.enable_model_drag_dest([target2,target4], Gdk.DragAction.MOVE)
        self.connect("drag-data-received", self.on_drag_data_received)
        # self.connect("drag-motion", self.on_drag_motion)
        # self.connect("drag-leave", self.on_drag_leave)

    def on_drag_leave(self, widget, context, time):
        """
            @param row as RowDND
            @param context as Gdk.DragContext
            @param time as int
        """
        widget.get_style_context().remove_class("drag-up")
        # row.get_style_context().remove_class("drag-down")

    def on_drag_motion(self, widget, context, x, y, time):
        # path, pos = self.get_drag_dest_row()
        # print(path, pos)
        # path = self.get_dest_row_at_pos(x,y)
        # print(x,y)
        widget.get_style_context().add_class("drag-up")
        # row.get_style_context().remove_class("drag-downg")

    def on_key_pressed(self, widget, event):
        # Gdk.ModifierType.CONTROL_MASK = 4
        if (4 & event.state) and (event.keyval == 97):
            dialog = DialogExample(self.get_toplevel())
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                name = dialog.entry.get_text()
                selection = widget.get_selection()
                model, iter = selection.get_selected()
                parent_path = model[iter][1]
                rowcount, treepath = Query.new_folder(parent_path, name)
                qu = Query.get_tree(treepath)
                model.init(qu, iter)
            elif response == Gtk.ResponseType.CANCEL:pass
            dialog.destroy()

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        selection = widget.get_selection()
        model, iter = selection.get_selected()

        if str(data.get_target()) == 'FOLDER':
            path = model.get_path(iter)
            string = f"{path.to_string()};{model[iter][1]}"
            data.set(data.get_target(), 8, bytes(string, "utf-8"))
        else:
            data.set(data.get_target(), 8, bytes(model[iter][1], "utf-8"))


    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        model = widget.get_model()
        # if str(data.get_target()) == 'FOLDER':
        #     drag_string, drag_folderpath = data.get_data().decode("utf-8").split(';')
        #     pos = widget.get_dest_row_at_pos(x, y)
        #     if pos:
        #         drop_path, position = pos
        #         drag_path = Gtk.TreePath.new_from_string(drag_string)
        #         action = drag_context.get_actions()

        #         drop_iter = model.get_iter(drop_path)

        #         # drag_iter = model.get_iter_from_string(drag_string)
        #         if (drop_path.compare(drag_path) == 0)\
        #         or (drop_path.is_descendant(drag_path))\
        #         : # equal
        #             drag_context.finish(False, False, time)
        #             return


        #         if position == 2 or position == 3:
        #             # into
        #             # make this parent
        #             if (action & Gdk.DragAction.MOVE) == Gdk.DragAction.MOVE:
        #                 # is_created, branch_query = 
        #                 rowcount, treepath = Query.set_folder_parent(model[drop_iter][1], drag_folderpath)
        #                 # print(is_created)
        #                 if rowcount:
        #                     # model.append(drop_iter, (model[drag_iter][0], model[drag_iter][1]))
        #                     # model.init(drop_iter, model[drop_iter][1], branch_query)
        #                     qu = Query.get_tree(treepath)
        #                     model.init(qu, root_iter=drop_iter)
        #                     if not widget.row_expanded(drop_path):
        #                         widget.expand_row(drop_path, False)
        #                     drag_context.finish(True, True, time)
        #                 else:
        #                     drag_context.finish(False, False, time)
        #             else:
        #                 drag_context.finish(False, False, time)
        #             # if (action & Gdk.DragAction.COPY) == Gdk.DragAction.COPY:
        #             #     # ask make synonym
        #             #     pass
        #         else:pass
        if str(data.get_target()) == 'TAG':
            drag_string = data.get_data().decode("utf-8")
            pos = widget.get_dest_row_at_pos(x, y)
            if pos:
                drop_path, position = pos
                if position == 2 or position == 3:
                    drop_iter = model.get_iter(drop_path)
                    tag_id = int(drag_string)
                    folder_id = model[drop_iter][0]
                    if Query.set_folder(tag_id, folder_id):
                        drag_context.finish(True, True, time)
                else:
                    drag_context.finish(False, False, time)
            else:
                drag_context.finish(False, False, time)


                        

    def on_menu_filenames_activate(self, widget, *args):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        # self.emit('tag-read', model[iter][0], model[iter][1])
        self.emit('filenames', model[iter][0])

    def on_menu_read_activate(self, widget, *args):
        # selection = self.get_selection()
        # model, iter = selection.get_selected()
        # self.emit('tag-read', model[iter][0], model[iter][1])
        self.emit('tag-read')

    def on_menu_update_activate(self, widget, *args):
        # selection = self.get_selection()
        # model, iter = selection.get_selected()
        # self.emit('tag-update', model[iter][0], model[iter][1])

        self.emit('tag-update')#tag_id
        # somewhere updated
        # update model in here or there?

    def on_menu_new_activate(self, widget, *args):
            dialog = DialogExample(self.get_toplevel())
            response = dialog.run()

            if response == Gtk.ResponseType.OK:
                name = dialog.entry.get_text()
                selection = self.get_selection()
                model, iter = selection.get_selected()
                parent_path = model[iter][1]
                rowcount, treepath = Query.new_folder(parent_path, name)
                qu = Query.get_tree(treepath)
                model.init(qu, iter)
            elif response == Gtk.ResponseType.CANCEL:pass
            dialog.destroy()

    def on_menu_delete_activate(self, widget, *args):
        # sure
        # db del
        # self del
        selection = self.get_selection()
        model, iter = selection.get_selected()
        try:
            Query.delete_folder(model[iter][1])
            model.remove(iter)
        except:pass

    def do_button_press_event(self, event):
        if event.button == Gdk.BUTTON_SECONDARY:
            selection = self.get_selection()
            pos = self.get_path_at_pos(event.x, event.y)# path, column, cell_x, cell_y
            if pos:
                #clicked any content
                path, column, cell_x, cell_y = pos
                if selection.path_is_selected(path):
                    #clicked in selection
                    self.dirmenu.popup(None, None, None, None, event.button, event.time)
                else:
                    #clicked outside of selection
                    Gtk.TreeView.do_button_press_event(self, event)
                    self.dirmenu.popup(None, None, None, None, event.button, event.time)
            else:
                #clicked empty area
                selection.unselect_all()
                return False
        else:
            Gtk.TreeView.do_button_press_event(self, event)



# class FileEdit(Gtk.Grid):
#     # __gsignals__ = {
#     #     'backed': (GObject.SIGNAL_RUN_FIRST, None, ()),
#     # }
#     def __init__(self):
#         Gtk.Grid.__init__(self, row_spacing=5, column_spacing=5)
#         self.set_property('margin-right', 5)
#         self.set_property('margin-left', 5)
#         main_model.connect('type-changed', self.on_model_type_changed)

#         # COMMANDS
#         command_box = Gtk.Box.new(orientation=1, spacing=0)
#         command_box.get_style_context().add_class("linked")
#         self.attach(command_box, 0, 0, 1, 1)

#         button = Gtk.Button('Open')
#         button.connect('clicked', self.on_open_clicked)
#         command_box.pack_start(button, False, True, 0)

#         button = Gtk.Button('Mcomix')
#         button.connect('clicked', self.on_mcomix_clicked)
#         command_box.pack_start(button, False, True, 0)

#         button = Gtk.Button('Open Folder')
#         button.connect('clicked', self.on_openf_clicked)
#         command_box.pack_start(button, False, True, 0)

#         button = Gtk.Button('Delete Entry')
#         button.connect('clicked', self.on_del_entry_clicked)
#         command_box.pack_start(button, False, True, 0)

#         button = Gtk.Button('Trash File & Entry')
#         button.connect('clicked', self.on_del_file_entry_clicked)
#         command_box.pack_start(button, False, True, 0)

#         button = Gtk.Button('Info List')
#         button.connect('clicked', self.on_info_clicked)
#         command_box.pack_start(button, False, True, 0)

#         #FILE INFOS
#         info_box = Gtk.Box.new(orientation=1, spacing=4)
#         info_box.set_hexpand(True)
#         self.attach(info_box, 1, 0, 1, 1)

#         button = Gtk.Button()
#         # button.set_halign(1)
#         button.set_relief(2)
#         img = Gtk.Image.new_from_file('')
#         fe_model.bind_property('imgfile', img, 'file', 0)
#         button.set_image(img)
#         button.connect('clicked', self.on_rethumb)
#         info_box.pack_start(button, False, True, 0)

#         label = Gtk.Label()
#         fe_model.bind_property('id', label, 'label', 0)
#         label.set_halign(1)
#         info_box.pack_start(label, False, True, 0)

#         label = Gtk.Label()
#         fe_model.bind_property('filename', label, 'label', 0)
#         label.set_halign(1)
#         label.set_line_wrap(True)
#         label.set_alignment(0,.5)
#         label.set_selectable(True)
#         info_box.pack_start(label, False, True, 0)

#         label = Gtk.Label()
#         fe_model.bind_property('filepath', label, 'label', 0)
#         label.set_line_wrap(True)
#         label.set_halign(1)
#         label.set_alignment(0,.5)
#         label.set_selectable(True)
#         info_box.pack_start(label, False, True, 0)

#         label = Gtk.Label('size')
#         fe_model.bind_property('size', label, 'label', 0)
#         label.set_halign(1)
#         info_box.pack_start(label, False, True, 0)

#         label = Gtk.Label('mtime')
#         fe_model.bind_property('mtime', label, 'label', 0)
#         label.set_halign(1)
#         info_box.pack_start(label, False, True, 0)

#         entry = Gtk.Entry()
#         fe_model.bind_property('thumbpath', entry, 'text', 1)
#         entry.set_placeholder_text('thumbpath')
#         info_box.pack_start(entry, False, True, 0)

#         entry = Gtk.Entry()
#         entry.set_placeholder_text('set')
#         fe_model.bind_property('set', entry, 'text', 1)
#         info_box.pack_start(entry, False, True, 0)

#         entry = Gtk.Entry()
#         entry.set_placeholder_text('note')
#         fe_model.bind_property('note', entry, 'text', 1)
#         info_box.pack_start(entry, False, True, 0)

#         entry = Gtk.SpinButton.new_with_range(0,100,1)
#         entry.set_placeholder_text('rating')
#         fe_model.bind_property('rating', entry, 'value', 1)
#         info_box.pack_start(entry, False, True, 0)

#         button = Gtk.Button('Update')
#         button.set_halign(1)
#         button.connect('clicked', self.on_update)
#         info_box.pack_start(button, False, True, 0)

#         #TAGS
#         tagbox = Gtk.Box.new(orientation=1, spacing=2)
#         self.attach(tagbox, 2, 0, 1, 1)

#         # label = Gtk.Label('Tags:')
#         # tagbox.pack_start(label, False, True, 0)
        
#         tagview = TagView()
#         tagview.connect('tag-delete', self.on_tag_delete)
#         tagview.connect('tag-read', self.on_tag_read)
#         tagview.connect('tag-update', self.on_tag_update)
#         tagview.set_model(fe_model.t_model)
#         # tagview.set_vexpand(True)
#         scrolled = Gtk.ScrolledWindow()
#         scrolled.set_vexpand(True)
#         scrolled.set_property('shadow-type', 1)
#         scrolled.add(tagview)
#         tagbox.pack_start(scrolled, True, True, 0)

#         hbox = Gtk.Box.new(orientation=0, spacing=0)
#         hbox.get_style_context().add_class("linked")

#         entry = Gtk.Entry()
#         comp = Gtk.EntryCompletion()
#         comp.set_text_column(1)
#         comp.set_model(tag_store)
#         entry.set_completion(comp)
#         hbox.pack_start(entry, True, True, 0)

#         button = Gtk.Button()
#         img = Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.MENU)
#         button.set_image(img)
#         button.connect('clicked', self.on_add_tag_clicked, entry)
#         hbox.pack_start(button, False, True, 0)

#         tagbox.pack_start(hbox, False, True, 0)


#         #RECOMMENDS
#         label = Gtk.Label('Suggestions:')
#         tagbox.pack_start(label, False, True, 0)
      
#         tagview = TagView()
#         tagview.connect('row-activated', self.on_recommend_activated)
#         tagview.set_model(fe_model.r_model)
#         scrolled = Gtk.ScrolledWindow()
#         # scrolled.set_hexpand(True)
#         scrolled.set_vexpand(True)
#         scrolled.set_property('shadow-type', 1)
#         scrolled.add(tagview)
#         tagbox.pack_start(scrolled, True, True, 0)

#         #INFOBAR
#         info = Gtk.InfoBar()
#         message_label = Gtk.Label('Done')
#         # info.
#         info.connect('response', self.on_info_response, message_label)
#         info.set_revealed(False)
#         info.set_show_close_button(True)
#         self.info = info
#         c = info.get_content_area()
#         c.add(message_label)
#         self.attach(info, 0, 20, 3, 1)
#         # box.pack_start(info, False, True, 0)

#     def on_model_type_changed(self, obj):
#         if obj.query_type == QueryType.FILEUPDATE:
#             self.set_file_id(obj.query_int)

#     def on_info_response(self, info_bar, response_id, label):
#         print(response_id)
#         info_bar.set_revealed(True)
#         if response_id == 1:
#             label.set_label('Done')
#             def close(*args):
#                 info_bar.set_revealed(False)
#             GLib.timeout_add(2400, close, None)
#         elif response_id == 2:
#             label.set_label('Error')
#         else:
#             info_bar.set_revealed(False)


#     def set_file_id(self, id):
#         file = Query.get_file(id)
#         try:
#             fe_model.imgfile = f'/media/soni/1001/persistent/1001/thumbs/{file.id}.jpg'
#         except Exception as e:
#             pass
#         fe_model.id = file.id
#         fe_model.filename = file.filename
#         fe_model.filepath = file.filepath
#         fe_model.size = format_size(file.size)
#         fe_model.mtime = str(file.mtime)
#         fe_model.thumbpath = file.thumb if file.thumb != None else ""
#         fe_model.set = file.set if file.set != None else ""
#         fe_model.note = file.note if file.note != None else ""
#         fe_model.rating = file.rating
#         #
#         fe_model.t_model.clear()
#         for q in Query.file_tags(id):
#             fe_model.t_model.append(q)
#         fe_model.r_model.clear()
#         for q in Query.tag_findall(file.filename):
#             fe_model.r_model.append(q)

#     def on_tag_read(self, widget):
#         selection = widget.get_selection()
#         model, iter = selection.get_selected()
#         main_model.set_type(QueryType.TAG, model[iter][0], None)

#     def on_tag_update(self, widget):
#         selection = widget.get_selection()
#         model, iter = selection.get_selected()
#         main_model.set_type(QueryType.TAGUPDATE, model[iter][0], None)

#     def on_tag_delete(self, widget):
#         selection = widget.get_selection()
#         model, iter = selection.get_selected()
#         # model.remove_tag(iter)
#         r = Query.delete_file_tag('archives', fe_model.id, model[iter][0])
#         if r:
#             model.remove(iter)

#     # def on_back_button_clicked(self, widget):
#     #     self.emit('backed')

#     def on_rethumb(self,widget):
#         img = widget.get_image()
#         item = Query.get_file(fe_model.id)
#         dest = rethumb(item, 'archives')
#         print(dest)
#         img.set_from_file(dest)

#     def on_update(self, widget):
#         r = Query.update_file(
#             media='archives',
#             index=fe_model.id,
#             thumb=fe_model.thumbpath,
#             set=fe_model.set,
#             note=fe_model.note,
#             rating=fe_model.rating,
#             )
#         if r > 0: 
#             self.info.set_message_type(0)
#             self.info.response(1)
#         else:
#             self.info.set_message_type(3)
#             self.info.response(2)

#     def on_recommend_activated(self, widget, path, column):
#         selection = widget.get_selection()
#         model, iter = selection.get_selected()
#         alias, tag_id, is_created = Query.add_file_tag('archives', fe_model.id, tagname=model[iter][1])
#         fe_model.t_model.append((tag_id, alias,))

#     def on_add_tag_clicked(self,widget, entry):
#         text = entry.get_text()
#         alias, tag_id, is_created = Query.add_file_tag('archives', fe_model.id, tagname=text)
#         fe_model.t_model.append((tag_id, alias,))
#         # fe_model.t_model.add_tag('archives', fe_model.id, text)
#         entry.set_text("")

#     def on_open_clicked(self,widget):
#         open_file(fe_model.filepath, 'default')

#     def on_openf_clicked(self,widget):
#         open_file(fe_model.filepath, 'folder')

#     def on_mcomix_clicked(self,widget):
#         open_file(fe_model.filepath, 'mcomix')

#     def on_del_entry_clicked(self,widget):
#         #DIALOG
#         dialog = QuestionDialog(self, f"file_id: \'{fe_model.id}\'")
#         response = dialog.run()

#         if response == Gtk.ResponseType.YES:
#             r = Query.delete_file(fe_model.id)
#             if r:
#                 main_model.back()
#         elif response == Gtk.ResponseType.NO:pass
#         dialog.destroy()

#     def on_del_file_entry_clicked(self,widget):
#         #DIALOG
#         dialog = QuestionDialog(self, f"file_id: \'{fe_model.id}\', \'{fe_model.filepath}\'")
#         response = dialog.run()

#         if response == Gtk.ResponseType.YES:
#             r = trash_file(fe_model.filepath)
#             if not r:#0 success
#                 r = Query.delete_file(fe_model.id)
#                 if r:
#                     main_model.back()
#         elif response == Gtk.ResponseType.NO:pass
#         dialog.destroy()

#     def on_info_clicked(self,widget):pass


# class HistorySwitcher(Gtk.Box):
#     def __init__(self):
#         Gtk.Box.__init__(self, orientation = 0 ,spacing=0)
#         self.get_style_context().add_class("linked")

#         img = Gtk.Image.new_from_icon_name('go-previous-symbolic', 2)
#         button = Gtk.Button(image=img)
#         button.set_sensitive(False)
#         main_model.bind_property('has_back', button, 'sensitive', 0)
#         button.connect('clicked', self.on_pre_clicked)
#         self.pack_start(button, False, False, 0)

#         img = Gtk.Image.new_from_icon_name('go-next-symbolic', 2)
#         button = Gtk.Button(image=img)
#         button.set_sensitive(False)
#         main_model.bind_property('has_forw', button, 'sensitive', 0)
#         button.connect('clicked', self.on_next_clicked)
#         self.pack_start(button, False, False, 0)

#     def on_pre_clicked(self, widget):
#         main_model.back()

#     def on_next_clicked(self, widget):
#         main_model.next()

class MediaSwitcher(Gtk.Button):
    media = GObject.Property(type=str, default="archives")
    def __init__(self):
        Gtk.Button.__init__(self)

        arc = Gtk.Image.new_from_icon_name('image-x-generic-symbolic', 2)
        vid = Gtk.Image.new_from_icon_name('applications-multimedia-symbolic', 2)

        self.connect('clicked', self.on_image_clicked, arc, vid)
        self.media = main_model.query_media
        main_model.bind_property('query_media', self, 'media', 1)

        #init
        if self.media == 'archives':
            self.set_image(vid)
        elif self.media == 'videos':
            self.set_image(arc)

    def on_image_clicked(self, widget, arc, vid):
        if self.media == 'archives':
            self.set_image(arc)
            self.media = 'videos'
        elif self.media == 'videos':
            self.set_image(vid)
            self.media = 'archives'


class ViewSwitcher(Gtk.Box):
    __gsignals__ = {
      'switched': (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    view = GObject.Property(type=str, default="gridview")

    def __init__(self):
        Gtk.Box.__init__(self, orientation = 0 ,spacing=0)
        self.get_style_context().add_class("linked")

        img = Gtk.Image.new_from_icon_name('view-list-symbolic', 2)
        togg_view1 = Gtk.ToggleButton(image=img)
        self.pack_start(togg_view1, False, False, 0)

        img = Gtk.Image.new_from_icon_name('view-grid-symbolic', 2)
        togg_view2 = Gtk.ToggleButton(image=img)
        self.pack_start(togg_view2, False, False, 0)

        togg_view1.connect('toggled', self.on_stack_toggled, "listview")
        togg_view2.connect('toggled', self.on_stack_toggled, "gridview")

        self.connect('notify::view', self.on_notify_view, togg_view1, togg_view2)

        #init
        self.set_widgets(self.view, togg_view1, togg_view2)

    def set_widgets(self, view, list_widget, grid_widget):
        if view == 'listview':
            grid_widget.set_active(False)
            grid_widget.set_sensitive(True)
            list_widget.set_sensitive(False)
        elif view == 'gridview':
            list_widget.set_active(False)
            list_widget.set_sensitive(True)
            grid_widget.set_sensitive(False)
        

    def on_notify_view(self, obj, gparamstring, list_widget, grid_widget):
        self.set_widgets(obj.view, list_widget, grid_widget)
        
    def on_stack_toggled(self, widget, view):
        if widget.get_active():
            self.set_property('view', view)
            self.emit('switched')
        else:pass


class Paginator(Gtk.Box):
    view = GObject.Property(type=str)
    def __init__(self):
        #TODO
        Gtk.Box.__init__(self, orientation = 0 ,spacing=0)
        self.get_style_context().add_class("linked")

        # button = Gtk.Button()
        # img = Gtk.Image.new_from_icon_name("go-previous-symbolic", Gtk.IconSize.MENU)
        # button.set_image(img)
        # # self.previous.set_sensitive(False)
        # pbox.pack_start(button, False, True, 0)
        # # pbox.set_size_request(80,-1)

        spin_button = Gtk.SpinButton.new_with_range(0,9999,1)
        # entry.set_size_request(20,12)
        spin_button.set_property('width-request', 20)
        main_model.bind_property('page', spin_button, 'value', 1)
        hbox.pack_start(spin_button, False, False, 0)
        # button = Gtk.Button()
        # img = Gtk.Image.new_from_icon_name("go-next-symbolic", Gtk.IconSize.MENU)
        # button.set_image(img)
        # # self.next.set_sensitive(False)
        # pbox.pack_start(button, False, True, 0)
        # hbox.pack_start(pbox, False, True, 0)

    def on_stack_toggled(self, widget, list_widget, grid_widget):
        if widget.get_active():
            if widget == list_widget:
                grid_widget.set_active(False)
                grid_widget.set_sensitive(True)
                list_widget.set_sensitive(False)
                self.set_property('view', 'listview')
            else:
                list_widget.set_active(False)
                list_widget.set_sensitive(True)
                grid_widget.set_sensitive(False)
                self.set_property('view', 'gridview')
        else:pass


# class IconTagView(Gtk.IconView):
#     def __init__(self):
#         Gtk.IconView.__init__(self, has_tooltip=True)

#         self.set_item_width(0)
#         self.set_row_spacing(0)
#         self.set_column_spacing(0)

#         renderer = Gtk.CellRendererPixbuf()
#         self.pack_start(renderer, False)
#         # renderer.set_alignment(0, 0)
#         self.add_attribute(renderer,'pixbuf', 2)

#         srenderer = Gtk.CellRendererText()
#         self.pack_start(srenderer, False)
#         srenderer.set_property('font','Ubuntu 9')
#         srenderer.set_property('ellipsize', 2)
#         srenderer.set_property('max-width-chars', 10)
#         self.add_attribute(srenderer,'text', 1)

    # def do_button_press_event(self, event):
    #     if event.button == Gdk.BUTTON_SECONDARY:
    #         selection = self.get_selected_items()
    #         path = self.get_path_at_pos(event.x, event.y)
    #         # selection = self.get_selection()
    #         # pos = self.get_path_at_pos(event.x, event.y)# path, column, cell_x, cell_y
    #         if path:
    #             #clicked any content
    #             if path in selection:
    #                 #clicked in selection
    #                 self.dirmenu.popup(None, None, None, None, event.button, event.time)
    #             else:
    #                 #clicked outside of selection
    #                 # Gtk.IconView.do_button_press_event(self, event)
    #                 self.unselect_all()
    #                 self.select_path(path)

    #                 self.dirmenu.popup(None, None, None, None, event.button, event.time)
    #         else:
    #             #clicked empty area
    #             self.unselect_all()
    #             return False
    #     else:
    #         Gtk.IconView.do_button_press_event(self, event)

class IconView(Gtk.IconView):
    __gsignals__ = {
      'file-read': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
      'file-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
      # 'edit': (GObject.SIGNAL_RUN_FIRST, None, (object, object,)),
    }
    def __init__(self):
        Gtk.IconView.__init__(self, has_tooltip=True)
        self.set_item_width(0)
        self.set_property('margin',0)
        self.set_row_spacing(0)
        self.set_column_spacing(0)
        self.set_item_padding(1)
        # self.accel = accel

        # self.connect('query-tooltip', self.on_tooltip_queried)

        # renderer = Gtk.CellRendererPixbuf()
        renderer = Gtk.CellRendererPixbuf()
        self.pack_start(renderer, False)
        renderer.set_alignment(0, 0)
        # self.thumb_renderer = renderer
        self.add_attribute(renderer,'pixbuf', 8)
        # self.add_attribute(renderer,'mime',StoreMainPosition.MIME)
       # self.set_cell_data_func(renderer,PixbufCellLayoutDataFunc,None)

        # srenderer = Gtk.CellRendererText()
        # self.pack_start(srenderer, False)
        # srenderer.set_property('font','Ubuntu 9')
        # srenderer.set_property('ellipsize', 2)
        # # srenderer.set_alignment(0.5, 0.5)
        # srenderer.set_property('max-width-chars', 10)
        # self.add_attribute(srenderer,'text', 5)
        
        # trenderer = Gtk.CellRendererText()
        # self.pack_start(trenderer, False)
        # self.add_attribute(trenderer,'text',StoreMainPosition.FILENAME)
        # # self.set_cell_data_func(trenderer,FileCellLayoutDataFunc,None)
        # trenderer.set_property('font','Ubuntu 9')
        # trenderer.set_alignment(0.5, 0.5)
        # trenderer.set_property('foreground','grey')
        # trenderer.set_property('ellipsize', 2)
        # trenderer.set_property('max-width-chars', 10)

        menu = Gtk.Menu()
        read = Gtk.MenuItem.new_with_label('Read')
        read.connect('activate', self.on_menu_read_activate)
        menu.append(read)
        update = Gtk.MenuItem.new_with_label('Update')
        update.connect('activate', self.on_menu_edit_activated)
        menu.append(update)
        menu.show_all()
        self.dirmenu = menu

        self.connect('item-activated', self.on_menu_edit_activated)

    def on_menu_read_activate(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if paths:
            path = paths[0]
            iter = model.get_iter(path)
        self.emit('file-read', model[iter][0])

    def on_menu_edit_activated(self, widget, *args):
        paths = self.get_selected_items()
        model = self.get_model()
        if not len(paths) >= 2:
            iter = model.get_iter(paths[0])
            self.emit('file-update', model[iter][0])

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
                    self.dirmenu.popup(None, None, None, None, event.button, event.time)
                else:
                    #clicked outside of selection
                    # Gtk.IconView.do_button_press_event(self, event)
                    self.unselect_all()
                    self.select_path(path)

                    self.dirmenu.popup(None, None, None, None, event.button, event.time)
            else:
                #clicked empty area
                self.unselect_all()
                return False
        else:
            Gtk.IconView.do_button_press_event(self, event)





# class TagEdit(Gtk.Grid):
#     __gsignals__ = {
#         'backed': (GObject.SIGNAL_RUN_FIRST, None, ()),
#         'list-tag': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
#     }
#     def __init__(self):
#         Gtk.Grid.__init__(self, row_spacing=5, column_spacing=5)
#         self.set_property('margin-right', 5)
#         self.set_property('margin-left', 5)
#         main_model.connect('type-changed', self.on_model_type_changed)


#         # COMMANDS
#         command_box = Gtk.Box.new(orientation=1, spacing=0)
#         command_box.get_style_context().add_class("linked")
#         self.attach(command_box, 0, 0, 1, 1)

#         # back_button = Gtk.Button('Back')
#         # command_box.pack_start(back_button, False, True, 0)
#         # back_button.connect('clicked', self.on_back_button_clicked)


#         button = Gtk.Button('List')
#         button.connect('clicked', self.on_list_clicked)
#         command_box.pack_start(button, False, True, 0)

#         button = Gtk.Button('Delete')
#         button.connect('clicked', self.on_del_clicked)
#         command_box.pack_start(button, False, True, 0)


#         #FILE INFOS
#         info_box = Gtk.Box.new(orientation=1, spacing=4)
#         info_box.set_hexpand(True)
#         self.attach(info_box, 1, 0, 1, 1)

#         button = Gtk.Button()
#         # button.set_halign(1)
#         button.set_relief(2)
#         img = Gtk.Image.new_from_file('')
#         ta_model.bind_property('thumbpath', img, 'file', 0)
#         button.set_image(img)
#         button.connect('clicked', self.on_rethumb)
#         info_box.pack_start(button, False, True, 0)

#         label = Gtk.Label()
#         ta_model.bind_property('id', label, 'label', 0)
#         label.set_halign(1)
#         info_box.pack_start(label, False, True, 0)


#         entry = Gtk.Entry()
#         ta_model.bind_property('name', entry, 'text', 1)
#         entry.set_placeholder_text('consistent tag name')
#         info_box.pack_start(entry, False, True, 0)

#         entry = Gtk.Entry()
#         ta_model.bind_property('thumb', entry, 'text', 1)
#         entry.set_placeholder_text('thumb number')
#         info_box.pack_start(entry, False, True, 0)

#         entry = Gtk.Entry()
#         entry.set_placeholder_text('note')
#         ta_model.bind_property('note', entry, 'text', 1)
#         info_box.pack_start(entry, False, True, 0)

#         entry = Gtk.SpinButton.new_with_range(0,100,1)
#         entry.set_placeholder_text('rating')
#         ta_model.bind_property('rating', entry, 'value', 1)
#         info_box.pack_start(entry, False, True, 0)

#         tags = TagsView2()
#         tags.set_model(ta_model.al_model)
#         # button.set_halign(1)
#         # button.connect('clicked', self.on_update)
#         info_box.pack_start(tags, False, True, 0)

#         button = Gtk.Button('Update')
#         button.set_halign(1)
#         button.connect('clicked', self.on_update)
#         info_box.pack_start(button, False, True, 0)

#         #ALIASES
#         tagbox = Gtk.Box.new(orientation=1, spacing=2)
#         self.attach(tagbox, 2, 0, 1, 1)

#         label = Gtk.Label('Aliases:')
#         tagbox.pack_start(label, False, True, 0)
        
#         tagview = TagView()
#         tagview.connect('row-activated', self.on_alias_read)
#         tagview.connect('tag-delete', self.on_alias_delete)
#         tagview.connect('tag-read', self.on_alias_read)
#         # tagview.connect('tag-update', self.on_alias_update)
#         tagview.set_model(ta_model.al_model)
#         # tagview.set_vexpand(True)
#         scrolled = Gtk.ScrolledWindow()
#         scrolled.set_vexpand(True)
#         scrolled.set_property('shadow-type', 1)
#         scrolled.add(tagview)
#         tagbox.pack_start(scrolled, True, True, 0)

#         hbox = Gtk.Box.new(orientation=0, spacing=0)
#         hbox.get_style_context().add_class("linked")

#         entry = Gtk.Entry()
#         comp = Gtk.EntryCompletion()
#         comp.set_text_column(1)
#         comp.set_model(tag_store)
#         entry.set_completion(comp)
#         hbox.pack_start(entry, True, True, 0)

#         button = Gtk.Button()
#         img = Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.MENU)
#         button.set_image(img)
#         button.connect('clicked', self.on_add_alias_clicked, entry)
#         hbox.pack_start(button, False, True, 0)

#         tagbox.pack_start(hbox, False, True, 0)


#         #COLLECTIONS
#         label = Gtk.Label('Collections:')
#         tagbox.pack_start(label, False, True, 0)
      
#         tagview = TagView()
#         tagview.connect('row-activated', self.on_col_read_activated)
#         tagview.connect('tag-read', self.on_col_read_activated)
#         tagview.connect('tag-delete', self.on_col_delete)
#         tagview.connect('tag-update', self.on_col_update)
#         tagview.set_model(ta_model.co_model)
#         scrolled = Gtk.ScrolledWindow()
#         # scrolled.set_hexpand(True)
#         scrolled.set_vexpand(True)
#         scrolled.set_property('shadow-type', 1)
#         scrolled.add(tagview)
#         tagbox.pack_start(scrolled, True, True, 0)

#         hbox = Gtk.Box.new(orientation=0, spacing=0)
#         hbox.get_style_context().add_class("linked")

#         entry = Gtk.Entry()
#         comp = Gtk.EntryCompletion()
#         comp.set_text_column(1)
#         comp.set_model(col_store)
#         entry.set_completion(comp)
#         hbox.pack_start(entry, True, True, 0)

#         button = Gtk.Button()
#         img = Gtk.Image.new_from_icon_name("list-add-symbolic", Gtk.IconSize.MENU)
#         button.set_image(img)
#         button.connect('clicked', self.on_add_col_clicked, entry)
#         hbox.pack_start(button, False, True, 0)

#         tagbox.pack_start(hbox, False, True, 0)

#         #INFOBAR
#         info = Gtk.InfoBar()
#         message_label = Gtk.Label('Done')
#         # info.
#         info.connect('response', self.on_info_response, message_label)
#         info.set_revealed(False)
#         info.set_show_close_button(True)
#         self.info = info
#         c = info.get_content_area()
#         c.add(message_label)
#         self.attach(info, 0, 20, 3, 1)

#     def on_rethumb(self, widget):
#         ta_model.thumbpath = f'/media/soni/1001/persistent/1001/thumbs/{ta_model.thumb}.jpg'



#     def on_info_response(self, info_bar, response_id, label):
#         print(response_id)
#         info_bar.set_revealed(True)
#         if response_id == 1:
#             label.set_label('Done')
#             def close(*args):
#                 info_bar.set_revealed(False)
#             GLib.timeout_add(2400, close, None)
#         elif response_id == 2:
#             label.set_label('Error')
#         else:
#             info_bar.set_revealed(False)

#     def on_model_type_changed(self, obj):
#         if obj.query_type == QueryType.TAGUPDATE:
#             self.set_tag_id(obj.query_int)

#     def set_tag_id(self, id):
#         file = Query.get_tag(id)
#         ta_model.id = file.id
#         ta_model.name = file.name if file.name != None else ""
#         ta_model.note = file.note if file.note != None else ""
#         ta_model.rating = file.rating
#         ta_model.thumb = file.thumb
#         ta_model.thumbpath = f'/media/soni/1001/persistent/1001/thumbs/{file.thumb}.jpg'
#         #
#         ta_model.al_model.clear()
#         for q in Query.get_tag_aliases(id):
#             ta_model.al_model.append(q)
#         ta_model.co_model.clear()
#         for q in Query.get_tag_collections(id):
#             ta_model.co_model.append(q)

#     # def on_alias_update(self, widget):pass
#     def on_alias_read(self, widget, *args):pass
#         # selection = widget.get_selection()
#         # model, iter = selection.get_selected()
#         # main_model.view = "listview"

#     def on_alias_delete(self, widget):
#         selection = widget.get_selection()
#         model, iter = selection.get_selected()

#         #DIALOG
#         dialog = QuestionDialog(self, f"alias_name: \'{model[iter][1]}\', alias_id: \'{model[iter][0]}\'")
#         response = dialog.run()

#         if response == Gtk.ResponseType.YES:
#             if Query.remove_tag_alias(model[iter][0]):
#                 model.remove(iter)
#         elif response == Gtk.ResponseType.NO:pass
#         dialog.destroy()

#     def on_add_alias_clicked(self, widget, entry):
#         text = entry.get_text()
#         tag_id = ta_model.id
#         alias, alias_id, is_created = Query.add_tag_alias(tag_id, text)
#         if is_created:
#             pass
#         ta_model.al_model.append((alias_id, alias,))
#         entry.set_text("")


#     def on_col_delete(self, widget):
#         selection = widget.get_selection()
#         model, iter = selection.get_selected()
#         col_id = model[iter][0]
#         tag_id = ta_model.id

#         #DIALOG
#         dialog = QuestionDialog(self, f"col_name: \'{model[iter][1]}\', col_id: \'{col_id}\', tag_id: \'{tag_id}\'")
#         response = dialog.run()

#         if response == Gtk.ResponseType.YES:
#             if Query.remove_tag_collection(tag_id, col_id):
#                 model.remove(iter)
#         elif response == Gtk.ResponseType.NO:pass
#         dialog.destroy()


#     def on_col_update(self, widget):pass
#     def on_add_col_clicked(self, widget, entry):
#         text = entry.get_text()
#         tag_id = ta_model.id
#         col_name, col_id, is_created = Query.add_tag_collection(tag_id, text)
#         if is_created:
#             col_store.append((col_id, col_name,))
#             #TODO select in view after new inserted?
#         ta_model.co_model.append((col_id, col_name,))
#         entry.set_text("")


#     def on_col_read_activated(self, widget):
#         selection = widget.get_selection()
#         model, iter = selection.get_selected()
#         col_model.set_col(model[iter][0])


#     def on_update(self, widget):
#         r = Query.update_tag(ta_model.id, ta_model.name, ta_model.note, ta_model.rating, ta_model.thumb)
#         if r > 0: 
#             self.info.set_message_type(0)
#             self.info.response(1)
#         else:
#             self.info.set_message_type(3)
#             self.info.response(2)

#     def on_list_clicked(self,widget):
#         self.emit('list-tag', ta_model.id)

#     def on_del_clicked(self,widget):
#         tag_id = ta_model.id

#         #DIALOG
#         dialog = QuestionDialog(self, f"tag_id: \'{tag_id}\'")
#         response = dialog.run()

#         if response == Gtk.ResponseType.YES:
#             if Query.delete_tag(tag_id):
#                 #TODO back?
#                 main_model.back()
#         elif response == Gtk.ResponseType.NO:pass
#         dialog.destroy()




