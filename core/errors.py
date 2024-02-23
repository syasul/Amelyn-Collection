from django.http import HttpResponse
from AmelynCollection import settings

class HTTPErrorMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    
class HTTPError(metaclass=HTTPErrorMeta):
    def error404(self, data):
        message = "Resource not found."
        if settings.DEBUG:
            message += f" {data}"
        return HttpResponse(message, status=404)
    
    def error500(self, data):
        message = "Internal server error."
        if settings.DEBUG:
            message += f" {data}"
        return HttpResponse(message, status=500)
    
    def error403(self, data):
        message = "Forbidden."
        if settings.DEBUG:
            message += f" {data}"
        return HttpResponse(message, status=403)
    
    def error401(self, data):
        message = "Unauthorized."
        if settings.DEBUG:
            message += f" {data}"
        return HttpResponse(message, status=401)
    
    def error400(self, data):
        message = "Bad request."
        if settings.DEBUG:
            message += f" {data}"
        return HttpResponse(message, status=400)