"""
ASGI config for stockproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# import os

# from channels.routing import ProtocolTypeRouter
# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockproject.settings')


# # Needed if starting server using daphne or uvicorn command
# import django
# django.setup()

# # Initialize Django ASGI application early to ensure the AppRegistry
# # is populated before importing code that may import ORM models.
# django_asgi_app = get_asgi_application()
# from channels.auth import AuthMiddlewareStack
# from mainapp.routing import websocket_urlPatterns

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     # Just HTTP for now. (We can add other protocols later.)
#     "websocket":AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlPatterns
#         )
#     )
# })


import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.sessions import SessionMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockproject.settings')

# Needed if starting server using daphne or uvicorn command
import django
django.setup()

from channels.auth import AuthMiddlewareStack
from mainapp.routing import websocket_urlpatterns
# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),
#     # Just HTTP for now. (We can add other protocols later.)
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket":  AuthMiddlewareStack(
                            SessionMiddlewareStack(
                               URLRouter(
            websocket_urlpatterns
        )
                               )                      
                    ),
})