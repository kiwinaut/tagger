import os
from gi.repository import GdkPixbuf
# import itertools
# from enums import Mime
def thumb_gen():
    Area = 192
    for entry in os.scandir('/home/soni/Pictures/pets'):
       if not entry.name.startswith('.') and entry.is_file():
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(entry.path)
            w = pixbuf.get_width()
            h = pixbuf.get_height()
            if w>h: 
                new_pixbuf = pixbuf.scale_simple(Area, Area*h/w,1)
            else:
                new_pixbuf = pixbuf.scale_simple(Area*w/h, Area,1)
            yield new_pixbuf

# sd={
# 'part1':[
#     'Ae',
#     'Cu',
#     'Di',
#     'Kri',
#     'Mo',
#     'Fam',],
# 'part2':[
#     'dar',
#     'kil',
#     'glar',
#     'tus',
#     'nic',
#     'tres',],
# }

# import random

# def name_gen():
#     first_part=sd['part1'][random.randint(0,len(sd['part1'])-1)]
#     second_part=sd['part2'][random.randint(0,len(sd['part2'])-1)]
#     return '{}{}'.format(first_part, second_part)

# def set_gen():
#     return 'Set {:03d}'.format(random.randint(1,99))

# def set_gen2():
#     return 'Set {:03d}'.format(random.randint(1,99))

# def mime_gen():
#     for i in [Mime.ARCHIVE, Mime.VIDEO, Mime.LIBIMAGE]:
#         yield i

# mgen = itertools.cycle(mime_gen())

