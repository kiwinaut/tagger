import argparse
import os
from constants import Mime
from vdbs.tracker_2_1 import __version__ as dbv

HOME = os.environ['HOME']
DIRPATH = os.path.dirname(os.path.realpath(__file__))

class ConfigManager(object):
    "Config manager"

    def __init__(self):
        self.defaults = {
            'testdatabase.path': f'{HOME}/.cache/tracker-{dbv}.db',

            'database.path': '%s/.cache/1001.db' % HOME,
            'logger.path': '%s/.cache/1001.log' % HOME,
            'css': '%s/static/main.css' % DIRPATH,
            'icon': '%s/static/tagger.png' % DIRPATH,
            'indexer.locations': ('/media/soni/1001/',),
            'indexer.thumb_location': '/media/soni/1001/.thumbnails',
            'indexer.size_threshold': 20000,
            'indexer.filters': [Mime.ARCHIVE, Mime.VIDEO],
            'indexer.thumb_size': (256,256,),
            'indexer.screenshot_size': (256,256,),
            'indexer.video_thumb_time': "00:59",
            'indexer.accepted_image_formats': (),
            'mount': '/media/soni/1001'
        }
        self.config = {}
        self.options = {}
        # self.arguments = []

    def index_parse(self):
        parser = argparse.ArgumentParser(description='terminal indexer', prog='vindexer')
        parser.add_argument('--findmax', action="store_false", help="Dont Find Max CTime")
        args = parser.parse_args()
        self.options['findmax'] = args.findmax

    def parse(self):
        parser = argparse.ArgumentParser(description='vip server', prog='vip')
        parser.add_argument('--test', action="store_true", help="Use Test Files")
        parser.add_argument('-p', '--port', type=int, metavar='8000', help="Port")

        args = parser.parse_args()
        self.options['test'] = args.test
        if args.test:
            self.options['database.path'] = ':memory:'



    def __setitem__(self, key, value, config=True):
        self.options[key] = value
        if config:
            self.config[key] = value

    def __getitem__(self, key):
        return self.options.get(key, self.config.get(key,
            self.defaults.get(key)))


CONFIG = ConfigManager()