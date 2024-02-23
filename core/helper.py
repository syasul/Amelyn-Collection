from django.http import HttpResponseRedirect

class HelperMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class Helper(metaclass=HelperMeta):
    def dd(self, data):
        from pprint import pprint
        pprint(data)