import os
import sys
from ucollections import OrderedDict

import filedb
from . import shared

_dbc = filedb.DB(shared.working_dir+"config")
_config = {}

class configTable(filedb.Model):

    # Create config table
    __db__ = _dbc
    __table__ = "config"
    __schema__ = OrderedDict([
        ("timestamp", filedb.now),
        ("name", "lmt"),
        ("unit",  0),
        ("port",  80),
        ("ssl",  "off"),
        ("password", ""),
        ("sleepenable", ""),
        ("sleeptime",  60),
        ("sleepfailure", ""),
        ("version", shared.__build__),
    ])

    @classmethod
    def getrow(cls):
        # if cached: return cached record
        if hasattr(cls,'_config'):  return cls._config
        # no cache: fetch it!
        try:
            cls._config = next(cls.get())
        except StopIteration:
            return None
        return cls._config