from curses import REPORT_MOUSE_POSITION
from xml.etree.ElementInclude import include
from django.contrib import admin

# Register your models here.


from .models import Message, Room, Topic


admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)