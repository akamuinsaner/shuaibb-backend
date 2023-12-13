from urllib import response
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if (response is not None):
        format = {}
        format["code"] = response.status_code
        if (response.data.get("detail") is None):
            format["message"] = response.data
        else:
            format["message"] = response.data.get("detail")
        response.data = format

    return response