from gi.repository import Gtk, GObject, Gdk
# from enums import FieldType
# from menus import TagMenu
import resources
# from gi.repository import GdkPixbuf
# import query
# from collections import namedtuple
# from query_interface import TagQuery
# from os.path import commonprefix
# from dialogs import EntryDialog, SureDialog, RelatedsDialog
from menus import CoreMenu

def cmp_path(old, new):
    sameness =  all([i==j for i,j in zip(old, new)])
    length = len(old) == len(new)
    # print(sameness, length)
    if sameness and length:
        #same
        return 0
    elif sameness and not length:
        #child
        return 2
        # return new[len(old):]
    else:
        #different
        return 1


class ColStore(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(
            self,
            int,     # id
            str,     # col_name
        )
        # self.set_sort_column_id(2, Gtk.SortType.ASCENDING)

class TagStore(Gtk.ListStore):
    def __init__(self):
        Gtk.ListStore.__init__(
            self,
            int,     # id
            str,     # col_name
        )
        # self.set_sort_column_id(2, Gtk.SortType.ASCENDING)



class DirStore(Gtk.TreeStore):
    # __gsignals__ = {
    # }
    def __init__(self):
        Gtk.TreeStore.__init__(
            self,
            int,     # 0 tag_id
            int,     # 0 category_id
            str,     # 1 label
            int,     # 0 ColType
            # str,     # 1 path
        )
        self.set_sort_column_id(2, Gtk.SortType.ASCENDING)
        # self.set_sort_func(7, ctime_sort_func, None)

    # def append_query(self, type, query, iter=None):
    #     self.clear()
    #     for q in query:
    #         self.append(iter, (type, q.label,))



    def append_tree(self, query):
        parent_stack = [('', None)]
        last_path = ''

        for q in query:
            if last_path != q.m_path:
                nodes = q.m_path.strip('/').split('/')
                for i, node in enumerate(nodes):
                    try:
                        parent_node, iter = parent_stack[i+1]
                    except:
                        parent_node = ''

                    if node == parent_node:
                        # 1 == (1, iter)[0]
                        continue
                    else:
                        # 2 == (1, iter)[0]
                        parent_stack = parent_stack[:i+1]
                        _, parent_iter = parent_stack[-1]
                        iter = self.append(parent_iter, (q.id, q.m_cat_id, q.m_cat, 0))
                        parent_stack.append((node, iter,))
                last_path = q.m_path

            _, parent_iter = parent_stack[-1]
            self.append(parent_iter, (q.id, q.m_cat_id, q.tag, 1))


    def append_branch(self, iter, query):
        for q in query:
            self.append(iter, (q.id, q.tag, q.type))

    def clear_branch(self, iter):
        first = self.iter_children(iter)
        if first is not None:
            while self.remove(first):
                pass

    def append_from_select(self, iter, field_type, query):
        # self.clear()
        # clean exists
        first = self.iter_children(iter)
        if first is not None:
            while self.remove(first):
                pass
        #
        for q in query:
            self.append(iter, (field_type, q.value,))

    def append_tags(self, iter, query_):
        first = self.iter_children(iter)
        if first is not None:
            while self.remove(first):
                pass
        for q in query_:
            self.append(iter, (1, q.tag,))
        
    def append_from_search(self, query_):
        parent_dict = {}
            # iter = self.append(None, (FieldType.SEARCH, value,))
        for q in query_:
            print(q.tag,q.set)
            if q.set is None:
                self.append(None, (1, q.tag,))
            else:
                try:
                    iter = parent_dict[q.set]
                except KeyError:
                    iter = self.append(None, (0, q.set, ))
                    parent_dict[q.set] = iter
                self.append(iter, (1, q.tag,))

        # return iter


def coltype_cell_data_func(tree_column, cell, tree_model, iter, data):
    type = tree_model[iter][2]
    if type == 0:
        cell.set_property('pixbuf', resources.folder_pixbuf)
    elif type == 1:
        cell.set_property('pixbuf', resources.tag_pixbuf)


class CollectionView(Gtk.TreeView):
    __gsignals__ = {
        'col-read': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'col-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    }
    def __init__(self):
        Gtk.TreeView.__init__(self)
        # self.get_selection().set_mode(3)

        column = Gtk.TreeViewColumn('name')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 1)
        self.append_column(column)

        self.set_property('headers-visible', False)

        menu = Gtk.Menu()
        read = Gtk.MenuItem.new_with_label('Read')
        read.connect('activate', self.on_menu_read_activate)
        menu.append(read)
        update = Gtk.MenuItem.new_with_label('Update')
        update.connect('activate', self.on_menu_update_activate)
        menu.append(update)
        menu.show_all()

        self.connect('row-activated', self.on_menu_read_activate)

        self.dirmenu = menu

    def on_menu_read_activate(self, widget, *args):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        self.emit('col-read', model[iter][0])
        # model.remove(iter)

    def on_menu_update_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        self.emit('col-update', model[iter][0])

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

class TagView(Gtk.TreeView):
    __gsignals__ = {
        'tag-read': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        'tag-update': (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    }
    def __init__(self):
        Gtk.TreeView.__init__(self)
        # self.get_selection().set_mode(3)

        column = Gtk.TreeViewColumn('name')
        renderer = Gtk.CellRendererText()
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 1)
        self.append_column(column)

        self.set_property('headers-visible', False)

        menu = Gtk.Menu()
        read = Gtk.MenuItem.new_with_label('Read')
        read.connect('activate', self.on_menu_read_activate)
        menu.append(read)
        update = Gtk.MenuItem.new_with_label('Update')
        update.connect('activate', self.on_menu_update_activate)
        menu.append(update)
        menu.show_all()

        self.connect('row-activated', self.on_menu_read_activate)

        self.dirmenu = menu

    def on_menu_read_activate(self, widget, *args):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        self.emit('tag-read', model[iter][0])
        # model.remove(iter)

    def on_menu_update_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        self.emit('tag-update', model[iter][0])

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


class DirView2(Gtk.TreeView):
    __gsignals__ = {
        'view-search': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        # 'search': (GObject.SIGNAL_RUN_FIRST, None, (object, object,)),
        # 'delete': (GObject.SIGNAL_RUN_FIRST, None, (object,)),
        'tag-selected': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
    }

    def __init__(self):
        Gtk.TreeView.__init__(self)
        # self.store.set_sort_column_id(1, Gtk.SortType.ASCENDING)
        # self.set_property('padding',4)

        column = Gtk.TreeViewColumn('name')
        # renderer = Gtk.CellRendererPixbuf()
        # renderer.set_property('font','Ubuntu 10')
        # column.pack_start(renderer, False)
        # column.add_attribute(renderer, 'pixbuf', 2)
        # column.set_cell_data_func(renderer, coltype_cell_data_func, func_data=None)
        # self.append_column(column)
        # self.set_expander_column(column)

        # column = Gtk.TreeViewColumn('tag')
        renderer = Gtk.CellRendererText()
        # renderer.set_property('font', 'Ubuntu 10')
        column.pack_start(renderer, True)
        column.add_attribute(renderer, 'text', 1)
        self.append_column(column)

        # self.set_show_expanders(False)
        # self.set_level_indentation(64)
        # self.set_activate_on_single_click(True)
        self.set_property('headers-visible', False)
        self.connect('row-activated', self.on_row_activated)

        # self.searchmenu = SearchMenu()
        # self.searchmenu.delete.connect('activate', self.on_search_delete_activate)

        # self.setmenu = SetMenu()
        # self.setmenu.new.connect('activate', self.on_dir_new_activate)
        # self.setmenu.change.connect('activate', self.on_dir_change_activate)
        # self.setmenu.delete.connect('activate', self.on_dir_delete_activate)

        # self.tagmenu = TagMenu()
        # self.tagmenu.new.connect('activate', self.on_tag_new_activate)
        # self.tagmenu.change.connect('activate', self.on_tag_rename_activate)
        # self.tagmenu.delete.connect('activate', self.on_tag_delete_activate)
        # self.tagmenu.makefolder.connect('activate', self.on_tag_makefolder_activate)
        # self.tagmenu.related.connect('activate', self.on_get_relateds)
        # self.tagmenu.info.connect('activate', self.on_info_activate)

        target2 = Gtk.TargetEntry.new('FOLDER', Gtk.TargetFlags.SAME_APP|Gtk.TargetFlags.SAME_WIDGET, 1)
        target3 = Gtk.TargetEntry.new('text/plain', Gtk.TargetFlags.SAME_WIDGET, 0)
        self.enable_model_drag_source(
            Gdk.ModifierType.BUTTON1_MASK|Gdk.ModifierType.CONTROL_MASK,
            [target2, target3],
            Gdk.DragAction.COPY|Gdk.DragAction.MOVE
        )
        # self.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)

        self.connect("drag-data-get", self.on_drag_data_get)
        
        self.enable_model_drag_dest([target2,target3], Gdk.DragAction.COPY|Gdk.DragAction.MOVE)
        self.connect("drag_data_received", self.on_drag_data_received)
        # self.get_style_context().add_class('dirview')
        # self.connect('drag-motion', self.on_drag_motion)
        # self.connect('drag_leave', self.on_drag_leave)
        # self.dirmenu.all.connect('activate', self.on_all_activate)

        # self.dirmenu.copy_text.connect('activate', self.on_copy_text_activate)
        # self.dirmenu.rename.connect('activate', self.on_rename_activate)
        # self.dirmenu.delete.connect('activate', self.on_delete_activate)

    def on_drag_leave(self, widget, context, time):
        widget.get_style_context().remove_class('view-motion')

    def on_drag_motion(self, widget, context, x, y, time):
        # widget.get_style_context().add_class('view-motion')
        pos = widget.get_dest_row_at_pos(x, y)
        # print(pos)
        if pos:
            self.set_drag_dest_row(*pos)

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        path = model.get_path(iter)
        # value = '{}\n{}'.format(*model.get(iter, 0, 1))
        value = path.to_string()
        if str(data.get_target()) == 'TAG':
            data.set(data.get_target(), 8, bytes(value, "utf-8"))

    def on_drag_data_received(self, widget, drag_context, x, y, data, info, time):
        model = widget.get_model()
        if str(data.get_target()) == 'FOLDER':
            drag_path = data.get_data().decode("utf-8")
            drag_iter = model.get_iter(drag_path)
            drag_id = model[drag_iter][0]
            drag_tag = model[drag_iter][1]
            # value = data.get_data()
            # drag_id, drag_tag = value.split('\n')
            pos = widget.get_dest_row_at_pos(x, y)
            if pos:
                drop_path, position = pos
                action = drag_context.get_actions()
                drop_iter = model.get_iter(drop_path)
                drop_type = model[drop_iter][2]
                drop_id = model[drop_iter][0]
                if drag_id == drop_id:
                    drag_context.finish(False, False, time)
                    return
                    
                        # dir
                if position == 2 or position == 3:
                    # into
                    # make this parent
                    if drop_type == 0:
                        if (action & Gdk.DragAction.MOVE) == Gdk.DragAction.MOVE:
                            if TagQuery.set_tag_parent(drag_tag, drop_id):
                                if widget.row_expanded(drop_path):
                                    model.append(drop_iter, (drag_id, drag_tag, model[drag_iter][2],))
                                drag_context.finish(True, True, time)
                            else:
                                drag_context.finish(False, False, time)
                        else:
                            drag_context.finish(False, False, time)
                    elif drop_type == 1:
                        if (action & Gdk.DragAction.COPY) == Gdk.DragAction.COPY:
                            # ask make synonym
                            pass
                else:
                    if (action & Gdk.DragAction.MOVE) == Gdk.DragAction.MOVE:
                        drop_iter_parent = model.iter_parent(drop_iter)
                        drag_iter_parent = model.iter_parent(drag_iter)
                        if drop_iter_parent == drag_iter_parent:
                            # do nothing
                            print('same')
                            # pass
                        else:
                            if drop_iter_parent:
                                drop_iter_parent_id = model[drop_iter_parent][0]
                            else:
                                drop_iter_parent_id = None
                            if TagQuery.set_tag_parent(drag_tag, drop_iter_parent_id):
                                print(drop_path)
                                if widget.row_expanded(model.get_path(drop_iter_parent)):
                                    model.append(drop_iter_parent, (drop_iter_parent_id, drag_tag, model[drag_iter][2],))
                                drag_context.finish(True, True, time)
                                print('moved')
                            else:
                                drag_context.finish(False, False, time)
                                print('failed')
                        

    def on_tag_makefolder_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        tag_id = model[iter][0]
        print(tag_id)
        tag_obj = TagQuery.set_type(tag_id, 0)
        print(tag_obj)
        if tag_obj:
            model[iter][2] = 0

    def on_tag_delete_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        tag = model[iter][1]

        dialog = SureDialog(self.get_toplevel())
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            TagQuery.delete_tag(tag)
            model.remove(iter)
            #TODO if type == folder model should be reset
        else:pass
        dialog.destroy()

    def on_tag_rename_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        old = model[iter][1]

        comp = Gtk.EntryCompletion()
        comp.set_text_column(0)
        comp.set_model(resources.tstore)
        dialog = EntryDialog(self.get_toplevel(), completion=comp)
        response = dialog.run()
        if response == 1:
            value = dialog.entry.get_text()
            if TagQuery.rename_tag(old, value):
                model[iter][1] = value.strip()
        else:pass
        dialog.destroy()
        

    # def on_tag_related_activate(self, widget):
    #     selection = self.get_selection()
    #     model, iter = selection.get_selected()
    #     tag = model[iter][1]
    #     # parent_iter = model.iter_parent(iter)
    #     # parent = model[parent_iter][1]
    #     # if parent == "~":
    #     #     parent = None
    #     dialog = RelatedsDialog(self.get_toplevel(), tag)
    #     response = dialog.run()
    #     if response == 1:
    #         value = dialog.get_selected().strip()
    #         print(value)
    #         # if value != "":
    #         #     res = Tags.create_tag(value, parent)
    #         #     if res:
    #         #         self.reload_model()
    #     else:pass
    #     dialog.destroy()

    def on_info_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        tag = model[iter][1] 

        res = TagQuery.info(tag)
        for r in res:
            print(r.m_count)

    def on_tag_new_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()

        type = model[iter][2]
        if type == 0:
            # if folder take this
            parent_id = model[iter][0]
        elif type == 1:
            # else find parent id else none
            parent_iter = model.iter_parent(iter)
            if parent_iter:
                parent_id = model[parent_iter][0]
            else:
                parent_id = None

        dialog = EntryDialog(self.get_toplevel())
        response = dialog.run()
        if response == 1:
            value = dialog.entry.get_text()
            # type = dialog.get_type()
            tag_obj = TagQuery.new_tag(value, parent_id)
            if tag_obj:
                if type == 0:
                    path = model.get_path(iter)
                    if self.row_expanded(path):
                        model.append(iter, (tag_obj.id, tag_obj.tag, tag_obj.type,))
                    else:
                        pass
                elif type == 1:
                    parent_iter = model.iter_parent(iter)
                    model.append(parent_iter, (tag_obj.id, tag_obj.tag, tag_obj.type,))
        else:
            pass
        dialog.destroy()

    def on_get_relateds(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        type = model[iter][2]
        if type == 1:
            tag_id = model[iter][0]
            query = TagQuery.get_relateds(tag_id)
            model.append_branch(iter, query)
            path = model.get_path(iter)
            self.expand_row(path, False)



    # def on_tag_set_activate(self, widget):
    #     selection = self.get_selection()
    #     model, iter = selection.get_selected()
    #     tag = model[iter][1]

    #     dialog = EntryDialog(self.get_toplevel())
    #     response = dialog.run()
    #     if response == 1:
    #         value = dialog.entry.get_text().strip()
    #         if value != "":
    #             Tags.set_parent(tag, value)
    #             self.reload_model()
    #     else:pass
    #     dialog.destroy()


    # def on_dir_delete_activate(self, widget):
    #     selection = self.get_selection()
    #     model, iter = selection.get_selected()
    #     set = model[iter][1]

    #     dialog = SureDialog(self.get_toplevel())
    #     response = dialog.run()
    #     if response == Gtk.ResponseType.OK:
    #         # TagSets.delete_set(set)
    #         self.reload_model()
    #     else:pass
    #     dialog.destroy()

    # def on_dir_change_activate(self, widget):
    #     selection = self.get_selection()
    #     model, iter = selection.get_selected()
    #     old = model[iter][1]

    #     dialog = EntryDialog(self.get_toplevel())
    #     response = dialog.run()
    #     if response == 1:
    #         value = dialog.entry.get_text().strip()
    #         if value != "":
    #             # TagSets.update_set(old, value)
    #             self.reload_model()
    #     else:pass
    #     dialog.destroy()
        

    # def on_dir_new_activate(self, widget):
    #     # selection = self.get_selection()
    #     # model, iter = selection.get_selected()
    #     dialog = EntryDialog(self.get_toplevel())
    #     response = dialog.run()
    #     if response == 1:
    #         value = dialog.entry.get_text().strip()
    #         if value != "":
    #             # res = TagSets.create_set(value)
    #             print(res)
    #             if res:
    #                 self.reload_model()
    #     else:pass
    #     dialog.destroy()

    def load_sets(self):
        qu = TagQuery.get_roots()
        model = self.get_model()
        model.append_roots(qu)

    def get_prop(self, model, iter):
        '''
        {ColType.NAME:value1, ColType.TAG:value2}
        '''
        query_prop = []

        #query properties
        col_type = model[iter][0]
        value = model[iter][1]
        # query_prop[col_type] = value
        query_prop.append(Prop(col_type, value, None))

        #recursivly find parent values
        child_iter = iter
        while True:
            parent_iter = model.iter_parent(child_iter)
            if parent_iter:
                # query_prop[model[parent_iter][0]] = model[parent_iter][1]
                query_prop.append(Prop(model[parent_iter][0], model[parent_iter][1], None))
                child_iter = parent_iter
            else:
                break
        return query_prop
        


    def on_search_delete_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        model.remove(iter)

    def on_dir_search_activate(self, widget, select_field):
        selection = self.get_selection()
        model, iter = selection.get_selected()

        parent_prop= self.get_prop(model, iter)
        qu = self.query.get_col(select_field, parent_prop)
        model.append_from_select(iter, select_field, qu)

        path = model.get_path(iter)
        self.expand_row(path, False)

    def on_all_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        prop = self.get_prop(model, iter)

        qu = self.query.get_files_new(prop)
        if qu:
            self.emit('view-search', qu)


    def on_rename_activate(self, widget):
        selection = self.get_selection()
        model, iter = selection.get_selected()
        value = model[iter][1]
        col_type = model[iter][0]
        #TODO
        # if col_type == FieldType.NAME:
        #     self.query.update_name(dict(name=value))
        # elif col_type == FieldType.GROUP:
        # elif col_type == FieldType.TAG:
        self.emit('update', iter, Prop(col_type, value, None))

    def on_delete_activate(self, widget):
        dialog = Gtk.Dialog(
            "Comfirm",
            self.get_toplevel(),
            0,
            (
                Gtk.STOCK_CANCEL,
                Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OK,
                Gtk.ResponseType.OK
            )
        )
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            selection = self.get_selection()
            model, iter = selection.get_selected()
            value = model[iter][1]
            select_column = model[iter][0]
            self.query.delete_col(select_column, value)
            model.remove(iter)
        elif response == Gtk.ResponseType.CANCEL:pass
        dialog.destroy()

    def on_copy_text_activate(self, widget):pass
    #TODO

    def on_row_activated(self, tree_view, path, column):
            model = self.get_model()
            iter = model.get_iter(path)
            type = model[iter][2]
            if type == 0:
                if self.row_expanded(path):
                    self.collapse_row(path)
                    model.clear_branch(iter)
                else:
                    parent_id = model[iter][0]
                    sq = TagQuery.get_branch(parent_id)
                    model.append_branch(iter, sq)
                    self.expand_row(path, False)
            elif type == 1:
                tag = model[iter][1]
                self.emit('tag-selected', tag)

    def do_button_press_event(self, event):
        if event.button == Gdk.BUTTON_SECONDARY:
            selection = self.get_selection()
            pos = self.get_path_at_pos(event.x, event.y)# path, column, cell_x, cell_y
            if pos:
                #clicked any content
                Gtk.TreeView.do_button_press_event(self, event)
                path, column, cell_x, cell_y = pos
                
                model, paths = selection.get_selected_rows()
                iter = model.get_iter(path)

                # query_prop= self.get_prop(model, iter)
                # if model[iter][0] == 0:
                #     self.setmenu.popup(None, None, None, None, event.button, event.time)
                # elif model[iter][0] == 1:
                    # self.dirmenu.set_prop(query_prop)
                self.tagmenu.popup(None, None, None, None, event.button, event.time)
            else:
                #clicked empty area
                selection.unselect_all()
                self.tagmenuempty.popup(None, None, None, None, event.button, event.time)
                # return False
        else:
            Gtk.TreeView.do_button_press_event(self, event)
            
