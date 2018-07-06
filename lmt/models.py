import os
import sys
from ucollections import OrderedDict, namedtuple
import ujson
import utime
import uos

import filedb
from . import shared

db = filedb.DB(shared.farm_dir+"db")

class BaseModel(filedb.Model):
    __db__ = db
    __table__ = None
    __schema__ = None
    __fields__ = None


    @classmethod
    def row(cls):
        try:
            return next(cls.rows())
        except StopIteration:
            return None
    
    @classmethod
    def json2row(cls, obj):
        return {k: obj.get(k) for k in cls.__fields__}
    
    @classmethod
    def init(cls, fail_silently=False):
        cls.__fields__ = list(cls.__schema__.keys())
        cls.Row = namedtuple(cls.__table__, cls.__fields__)
        for d in (cls.__db__.name, "%s/%s" % (cls.__db__.name, cls.__table__)):
            try:
                uos.mkdir(d)
            except OSError as e:
                if fail_silently:
                    print(e)
    
    @classmethod
    def save(cls, **kwargs):
        pkey_field = cls.__fields__[0]
        pkey_type = cls.__schema__[pkey_field]
        for k, v in cls.__schema__.items():
            if k not in kwargs:
                default = v
                if callable(default):
                    default = default()
                kwargs[k] = default

        pkey = kwargs[pkey_field]
        with open(cls.fname(pkey), "w") as f:
            f.write(ujson.dumps(kwargs))
        shared._log.info("model: create pkey: %s" % pkey)
        return kwargs
    
    @classmethod
    def rows(cls):
        cls.Row = namedtuple(cls.__table__, cls.__fields__)
        try:
            for dirent in uos.ilistdir("%s/%s" % (cls.__db__.name, cls.__table__)):
                fname = dirent[0]
                if fname[0] == ".":
                    continue
                with open(cls.fname(fname)) as f:
                    yield cls.json2row(ujson.loads(f.read()))
        except OSError:
            return None
    
    @classmethod
    def update(cls, where, **fields):
        pkey_field = cls.__fields__[0]
        assert pkey_field in where
        print("update:", where[pkey_field])
        with open(cls.fname(where[pkey_field])) as f:
            data = ujson.loads(f.read())
        for k in fields.keys():
            if not k.startswith('__'):
                if k not in data.keys():
                    del fields[k]
            else:
                fields[k.replace('__', '')] = fields[k]
        data.update(fields)
        with open(cls.fname(where[pkey_field]), "w") as f:
            f.write(ujson.dumps(data))
    
    @classmethod
    def delete(cls, pkey, fail_silently=False):
        fname = cls.fname(pkey)
        try:
            uos.remove(fname)
        except OSError as e:
            if fail_silently:
                print(e)
    


class WifiAPModel(BaseModel):
    __table__ = "wifiap"
    __schema__ = OrderedDict([
        ("created_at", str(int(utime.time()))),
        ("channel", 11),
        ("hidden", False),
        ("authmode", 4),
        ("essid", "geekgarden"),
        ("password", "mysupersecretpass"),
        ("hostname", "geekgarden"),
        ("ip", "192.168.10.1"),
        ("mask", "255.255.255.0"),
        ("gateway", "192.168.10.1"),
        ("dns", "8.8.8.8"),
    ])
    __fields__ = list(__schema__.keys())

