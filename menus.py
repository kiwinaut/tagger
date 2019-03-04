from gi.repository import Gtk
# from enums import ColType

class CoreMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        create = Gtk.MenuItem.new_with_label('Create')
        self.append(create)

        read = Gtk.MenuItem.new_with_label('Read')
        self.append(read)

        update = Gtk.MenuItem.new_with_label('Update')
        self.append(update)

        delete = Gtk.MenuItem.new_with_label('Delete')
        self.append(delete)

        self.menus = (create, read, update, delete,)

        self.show_all()

class IconMenu(Gtk.Menu):
    def __init__(self):
        Gtk.Menu.__init__(self)

        self.open_file = Gtk.MenuItem.new_with_label('Open File')
        # menuitem.add_accelerator('activate', accel_group, 101, Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)
        self.append(self.open_file)

        self.open_loc = Gtk.MenuItem.new_with_label('Open Loc')
        # menuitem.add_accelerator('activate', accel_group, 101, Gdk.ModifierType.CONTROL_MASK, Gtk.AccelFlags.VISIBLE)
        self.append(self.open_loc)

        menuitem = Gtk.SeparatorMenuItem()
        self.append(menuitem)

        self.reload = Gtk.MenuItem.new_with_label('Reload')
        self.append(self.reload)

        self.rethumb = Gtk.MenuItem.new_with_label('ReThumb')
        self.append(self.rethumb)


        menuitem = Gtk.SeparatorMenuItem()
        self.append(menuitem)
        
        self.edit = Gtk.MenuItem.new_with_label('Edit')
        self.append(self.edit)

        #delete with
        sub_menu = Gtk.Menu()

        self.del_entry = Gtk.MenuItem.new_with_label('Entry')
        sub_menu.append(self.del_entry)

        self.del_both = Gtk.MenuItem.new_with_label('Entry with File')
        sub_menu.append(self.del_both)

        menuitem = Gtk.MenuItem.new_with_label('Delete')
        menuitem.set_submenu(sub_menu)

        self.append(menuitem)
        self.show_all()

class DirMenu(Gtk.Menu):

    def __init__(self):
        Gtk.Menu.__init__(self)

        menuitem = Gtk.MenuItem.new_with_label('All')
        self.append(menuitem)
        self.all = menuitem

        menuitem = Gtk.MenuItem.new_with_label('Group')
        self.append(menuitem)
        self.group = menuitem

        menuitem = Gtk.SeparatorMenuItem()
        self.append(menuitem)

        self.subs= []
        menuitem = Gtk.MenuItem.new_with_label('Names')
        self.append(menuitem)
        self.subs.append(menuitem)
        self.names = menuitem

        menuitem = Gtk.MenuItem.new_with_label('Groups')
        self.append(menuitem)
        self.subs.append(menuitem)
        self.groups = menuitem

        menuitem = Gtk.MenuItem.new_with_label('Tags')
        self.append(menuitem)
        self.subs.append(menuitem)
        self.tags = menuitem

        menuitem = Gtk.SeparatorMenuItem()
        self.append(menuitem)

        menuitem = Gtk.MenuItem.new_with_label('Collapse Parent')
        self.append(menuitem)
        self.collapse = menuitem

        menuitem = Gtk.MenuItem.new_with_label('Copy Text')
        self.append(menuitem)
        self.copy_text = menuitem

        menuitem = Gtk.MenuItem.new_with_label('Rename')
        self.append(menuitem)
        self.rename = menuitem

        menuitem = Gtk.MenuItem.new_with_label('Delete')
        self.append(menuitem)
        self.delete = menuitem

        self.show_all()

    # def set_prop(self, query_prop):
    #     for widget in self.subs:
    #         widget.show()
    #     for prop in query_prop:
    #         if prop[0] == ColType.NAME:
    #             self.subs[0].hide()
    #         elif prop[0] == ColType.GROUP:
    #             self.subs[1].hide()
    #         elif prop[0] == ColType.TAG:
    #             self.subs[2].hide()



class SearchMenu(Gtk.Menu):

    def __init__(self):
        Gtk.Menu.__init__(self)

        menuitem = Gtk.MenuItem.new_with_label('Delete')
        self.append(menuitem)
        self.delete = menuitem

        self.show_all()



