from django.urls import re_path, path

from . import cunsumers

websocket_urlpatterns = [
    # re_path(r'ws/stock/(?P<room_name>\w+)/$', cunsumers.StockConsumer.as_asgi()),
    # path(r'ws/stock/(?P<room_name>\w+)/$', cunsumers.StockConsumer.as_asgi()),
    path('ws/stock/<str:room_name>/', cunsumers.StockConsumer.as_asgi()),

]