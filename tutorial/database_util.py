import json
from sqlalchemy.ext.declarative import DeclarativeMeta
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        print "default"
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    print data
                    print field

                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
#            return json.JSONEncoder().encode(fields)
            return fields
    
        return json.JSONEncoder.default(self, obj)

