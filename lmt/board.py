from . import shared

class Board:
    def __init__(self):
        self.log = shared._log
        self.__platform = self.get_platform()
        self.__id = self.get_id()
    
    @property
    def platform(self):
        return self.__platform
    
    @property
    def id(self):
        return self.__id
    
    @property
    def time(self):
        import utime
        return utime.mktime(utime.localtime())
    
    def get_platform(self):
        import sys
        return sys.platform
    
    def get_id(self):
        import machine
        from ubinascii import hexlify
        return hexlify(machine.unique_id()).decode('utf-8')
