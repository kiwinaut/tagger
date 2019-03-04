import subprocess as sp

def open_file(path, app):
    # try:
        if app == 'default':
            r = sp.call(["gio", "open", path])
        elif app =='mcomix':
            r = sp.call(["mcomix", path])
        elif app =='folder':
            r = sp.call(['nautilus', '-s', path])
        else:
            raise(Exception('no suitable app'))

def trash_file(path):
    r = sp.call(["gio", "trash", path])

def movetotemp():
    sp.call(['mv -i ~/Downloads/p/viper/*.tar /media/soni/1001/gals/temp3'], shell=True)
    sp.call(['vindex'])

