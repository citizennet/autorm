import json

class FieldBase(object):
    def __init__(self, name=None, default=None, index=False, notnull=False, primary_key=False, sql_type="TEXT"):
        self.name = name
        self.default = default
        self.index = index
        self.notnull = notnull
        self.primary_key = primary_key
        self.sql_type = sql_type
        
    def __eq__(self, b):
        if type(b) == str:
            return self.name == b
        return super(FieldBase, self).__eq__(b)
    
    def to_python(self, value):
        return value
    
    def to_db(self, value):
        return value
    
    def define(self):
        return "%s %s%s%s" % (self.name, 
                              self.sql_type,
                              self.default and " DEFAULT " + self.default or "", 
                              self.notnull and " NOT NULL" or "")
    
class Field(FieldBase):
    pass

class TextField(Field):
    pass

class IntegerField(Field):
    def __init__(self, **kwargs):
        kwargs['sql_type'] = 'INTEGER'
        super(IntegerField, self).__init__(self, **kwargs)

class FloatField(Field):
    def __init__(self, **kwargs):
        kwargs['sql_type'] = 'FLOAT'
        super(IntegerField, self).__init__(self, **kwargs)
        
class IdField(Field):
    def __init__(self, auto_increment=True):
        kwargs['sql_type'] = "INTEGER PRIMARY KEY" + (auto_increment and " AUTOINCREMENT" or "")
        super(IdField, self).__init__(self, **kwargs)
    
class JSONField(Field):
    def to_python(self, dbvalue):
        if not dbvalue: return None
        return json.loads(dbvalue)
    
    def to_db(self, pyvalue):
        if not pyvalue: return None
        return json.dumps(pyvalue)
