import logging
import uos

import gc

from . import models
from . import shared
from .models import _dbc
from .utils import utils

class Start(object):
    def __init__(self, level=logging.DEBUG):
        logging.basicConfig(level)
        shared._log = logging.getLogger('core')
        self._log = logging.getLogger('start')

        shared._log.info("start: Start constructor")
    
    def run(self):

        shared._utils = utils()
        # create dirs
        self.create_dirs()
        # connect db
        self.connect_db()
        # create tables
        self.create_tables()
    
    def create_dirs(self):
        root_dir = ""
        try:
            self._log.debug("Start: Create directory config")
            uos.mkdir(root_dir+"config")
        except OSError as e:
            self._log.debug("Start: Create directory config exception: "+repr(e))
        
        gc.collect()
    
    def connect_db(self):
        _dbc.connect()
    
    def create_tables(self):
        try:
            self._log.debug("Init: config Table")
            models.configTable.create_table(True)
        except OSError as e:
            self._log.error("Init: config Table exception: "+repr(e))
        gc.collect()
