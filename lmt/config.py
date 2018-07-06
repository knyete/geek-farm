import uos

from . import shared

class Config:
    def __init__(self, farm_dir=None):
        self.log = shared._log
        self.dir = farm_dir if farm_dir else shared.farm_dir
        self.log.debug("config: Start constructor")
    
    def makedirs(self):
        import gc
        try:
            self.log.debug("Config: Create directory")
            uos.mkdir(self.dir+"config")
        except OSError as e:
            self.log.error("Config: Create directory config exception: "+repr(e))
        gc.collect()