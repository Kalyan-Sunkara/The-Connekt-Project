from django.contrib import admin
from firstApp.models import UserProfileInfo, Question, Rooms
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Question)
admin.site.register(Rooms)
