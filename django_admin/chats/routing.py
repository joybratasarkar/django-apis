from django.urls import re_path

from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer.as_asgi()),
    # re_path(r'ws/video/(?P<video_room_id>\w+)/', consumers.VideoStreamingConsumer.as_asgi()),
        re_path(r'ws/video/(?P<room_name>\w+)/$', consumers.WebRTCConsumer.as_asgi()),

]
