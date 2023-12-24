from rest_framework import renderers

class CustomJsonRenderer(renderers.JSONRenderer):
    media_type = "application/json"
    format = "json"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context['response'].exception:
            data = {
                "success": True,
                "code": 0,
                "data": data,
            }
        return super(CustomJsonRenderer, self).render(data, accepted_media_type, renderer_context)