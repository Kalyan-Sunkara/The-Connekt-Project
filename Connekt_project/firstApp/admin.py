from django.contrib import admin
from firstApp.models import UserProfileInfo, Question, Rooms, Messages
# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(Question)
admin.site.register(Rooms)
admin.site.register(Messages)
