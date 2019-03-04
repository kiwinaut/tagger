from thumbnailer import clip
from thumbnailer.archive import Thumbnailer, archive_filename_parser
from config import CONFIG
from pathlib import Path

THUMB_SIZE = 300, 300
SCREENSHOT_SIZE = 1024, 768
VIDEOCUT = '0:09'
HEIGHT= 180


def rethumb(item, media, value=None):
    # fpath = '%s/%s' % (CONFIG['mount'], item.filepath)
    fpath = item.filepath
    if media == 'videos':
        clp = clip.Clip(fpath)
        # time = duration_to_int(value)
        if value:
            blob = clp.extract_frame(value, height=HEIGHT)
        else:
            blob = clp.extract_frame(VIDEOCUT, height=HEIGHT)
    elif media == 'archives':
        t = Thumbnailer(size=THUMB_SIZE)
        value = item.thumb.strip()
        if value:
            # blob = t.blob_bywidth(fpath, HEIGHT, infoname=value.strip())
            filename, location_int = archive_filename_parser(value)
            blob = t.blob_bysquare(fpath, infoname=filename, location=location_int)
        else:
            blob = t.blob_bysquare(fpath)
            # blob = t.blob_bywidth(fpath, HEIGHT)
    dest = '%s/%s/%s.jpg' % (CONFIG['mount'], 'persistent/1001/thumbs', item.id)
    with open (dest, 'wb') as fp:
        fp.write(blob)
    return dest

def videoretumb(item, value=None):
    if value:
        extime = value
    else:
        extime = VIDEOCUT
    clp = clip.Clip(fpath)
    blob = clp.extract_frame(extime, height=HEIGHT)

def new_screenshot(item):
    fpath = '%s/%s' % (CONFIG['mount'], item.filepath)
    clp = clip.Clip(fpath)
    blob = clp.screenshot(SCREENSHOT_SIZE[0], SCREENSHOT_SIZE[1])
    dest = '%s/%s/%s_s.jpg' % (CONFIG['mount'], 'persistent/1001/thumbs', item.id)
    with open (dest, 'wb') as fp:
        fp.write(blob)

