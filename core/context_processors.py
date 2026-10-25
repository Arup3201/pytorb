from django.conf import settings


def websocket_settings(request):
    return {
        "websocket_url": settings.WEBSOCKET_URL,
    }