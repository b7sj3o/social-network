from django.contrib import admin
from .models import BaseMessage, Friends


admin.site.register(BaseMessage)
admin.site.register(Friends)
