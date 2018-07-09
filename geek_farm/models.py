"""Models."""
from ucollections import OrderedDict
import ujson
import utime

import btreedb as uorm
import btree


db = uorm.DB("gf.db")

class WelcomeModel(uorm.Model):

    __db__ = db
    __table__ = "note"
    __schema__ = OrderedDict([
        ("timestamp", ("TIMESTAMP", uorm.now)),
        ("firsttime", ("INT", 0)),
    ])
