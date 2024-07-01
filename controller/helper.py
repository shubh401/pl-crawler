from config import *

def serialize_object(data):
    if isinstance(data, set):
        return list(data)
    elif isinstance(data, defaultdict):
        return dict(data)
    return data
