import logging
# import uos

import gc

# from . import models
from . import shared
# from .models import _dbc
# from .utils import utils
from .board import Board

class Start(object):
    def __init__(self, level=logging.DEBUG):
        logging.basicConfig(level)
        shared._log = logging.getLogger('core')
        self._log = logging.getLogger('start')

        shared._log.info("start: Start constructor")
    
    def run(self):
        shared._board = Board()
        gc.collect()
        # shared._utils = utils()
        # # create dirs
        # self.create_dirs()
        # # connect db
        # self.connect_db()
        # # create tables
        # self.create_tables()
        # # set default values db
        # self.set_default_values()
        # # set default network
    
    # def create_dirs(self):
    #     root_dir = ""
    #     try:
    #         self._log.debug("Start: Create directory config")
    #         uos.mkdir(root_dir+"config")
    #     except OSError as e:
    #         self._log.debug("Start: Create directory config exception: "+repr(e))
        
    #     gc.collect()
    
    # def connect_db(self):
    #     _dbc.connect()
    
    # def close_db(self):
    #     _dbc.close()
    
    # def create_tables(self):
    #     try:
    #         self._log.debug("Init: config Table")
    #         models.ConfigModel.create_table(True)
    #     except OSError as e:
    #         self._log.error("Init: config Table exception: "+repr(e))
    #     try:
    #         self._log.debug("Init: network Table")
    #         models.NetworkModel.create_table(True)
    #     except OSError as e:
    #         self._log.error("Init: network Table exception: "+repr(e))
        
    #     gc.collect()
    
    # def set_default_values(self):
    #     config = models.ConfigModel.get()
        
    #     if not config:
    #         self._log.debug("Init: Create Config Record")
    #         models.ConfigModel.create(name=shared.initial_name)

    #     network = models.NetworkModel.get()
        
    #     if not network:
    #         self._log.debug("Init: Create Network Record")
    #         models.NetworkModel.create(ssid="")

    #     self.close_db()

    #     gc.collect()
        
    # def run_network(self):
    #     pass

