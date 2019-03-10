import subprocess as sp

def open_file(path, app):
    sp.run(["test", "-e", path], check=True)
    # try:
    if app == 'default':
        sp.call(["gio", "open", path])
    elif app =='mcomix':
        sp.call(["mcomix", path])
    elif app =='folder':
        sp.call(['nautilus', '-s', path])
    else:
        raise(Exception('no suitable app'))

def trash_file(path):
    sp.run(["gio", "trash", path], check=True)

def movetotemp():
    sp.call(['mv -i ~/Downloads/p/viper/*.tar /media/soni/1001/gals/temp3'], shell=True)
    sp.call(['vindex'])

