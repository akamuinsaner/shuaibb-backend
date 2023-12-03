from rest_framework import renderers

class CustomJsonRenderer(renderers.JSONRenderer):
    media_type = "application/json"
    format = "json"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if (type(data) is dict and data.get("code") is not None and data.get("message") is not None):
            return super(CustomJsonRenderer, self).render(data, accepted_media_type, renderer_context)
        format = {
            "code": 0,
            "data": data,
        }
        return super(CustomJsonRenderer, self).render(format, accepted_media_type, renderer_context)