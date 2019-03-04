from enum import Enum

class Status(Enum):
    SLEEP = 0
    QUEUED = 1
    ACTIVE = 2
    SOLVING = 3
    DOWNLOAD = 4
    ERROR = 5

class Mime(Enum):
    ARCHIVE =   1
    VIDEO =     2
    LIBIMAGE =  3

MimeTypes = {
    '.mkv': Mime.VIDEO,
    '.mp4': Mime.VIDEO,
    '.mpg': Mime.VIDEO,
    '.mpeg': Mime.VIDEO,
    '.mov': Mime.VIDEO,
    '.mov': Mime.VIDEO,
    '.avi': Mime.VIDEO,
    '.wmv': Mime.VIDEO,
    '.lib.tar': Mime.LIBIMAGE,
    '.tar': Mime.ARCHIVE,
    '.tar.gz': Mime.ARCHIVE,
    '.zip': Mime.ARCHIVE,
    '.rar': Mime.ARCHIVE,
    # '.jpg': Mime.Image,
    # '.jpeg': Mime.Image,
    # '.jpg-large': Mime.Image,
    # '.png': Mime.Image,
    # '.gif': Mime.Image,
}