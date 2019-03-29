import argparse
import os
# from constants import Mime
from vdbs import tracker

tracker.requie_version('2.2')

HOME = os.environ['HOME']
DIRPATH = os.path.dirname(os.path.realpath(__file__))

class ConfigManager(object):

    def __init__(self):
        self.defaults = {
            'database.path': f'{HOME}/.cache/tracker-{tracker.__version__}.db',
            'database.version': f'{tracker.__version__}',
            # 'database.path': '%s/.cache/1001.db' % HOME,
            # 'logger.path': '%s/.cache/1001.log' % HOME,
            # 'css': '%s/static/{}' % DIRPATH,
            # 'icon': '%s/static/tagger.png' % DIRPATH,
            'static': '%s/static/{}' % DIRPATH,
            # 'indexer.locations': ('/media/soni/1001/',),
            # 'indexer.thumb_location': '/media/soni/1001/.thumbnails',
            # 'indexer.size_threshold': 20000,
            # 'indexer.filters': [Mime.ARCHIVE, Mime.VIDEO],
            # 'indexer.thumb_size': (256,256,),
            # 'indexer.screenshot_size': (256,256,),
            # 'indexer.video_thumb_time': "00:59",
            # 'indexer.accepted_image_formats': (),
            'mount': '/media/soni/1001',
            'indexer.thumb_location':'/media/soni/1001/persistent/1001/thumbs/{}.jpg',
            'query.page_limit': 150,
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
        # parser.add_argument('-p', '--port', type=int, metavar='8000', help="Port")

        args = parser.parse_args()
        self.options['test'] = args.test
        if args.test:
            self.options['testdatabase.path'] = f'{HOME}/.cache/tracker-{tracker.__version__}_test.db'
            self.options['database.version'] = f'{tracker.__version__}_test'



    def __setitem__(self, key, value, config=True):
        self.options[key] = value
        if config:
            self.config[key] = value

    def __getitem__(self, key):
        return self.options.get(key, self.config.get(key,
            self.defaults.get(key)))


CONFIG = ConfigManager()