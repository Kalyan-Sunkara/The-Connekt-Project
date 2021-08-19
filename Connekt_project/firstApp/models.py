from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import string
import random
# Create your models here.
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    FIELD = models.TextChoices('FIELDTYPE', 'Medical Engineering Education Home General')
    #additional
    USERTYPE = models.TextChoices('USERTYPE', 'User Specialist')
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    user_type = models.CharField(choices=USERTYPE.choices, max_length=10, default="User")
    field = models.CharField(choices=FIELD.choices, max_length=12, default="General")
    slug = models.SlugField(null=True)
    def get_type(self):
        return self.user.user_type
    def __str__(self):
        return self.user.username

class Question(models.Model):
    PROGRESSTYPE = models.TextChoices('PROGRESSTYPE', 'Active Pending Archived')
    FIELDTYPE = models.TextChoices('FIELDTYPE', 'Medical Engineering Education Home General')
    title = models.CharField(max_length=200)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    price = models.PositiveIntegerField(default=1)
    field_type = models.CharField(choices=FIELDTYPE.choices, max_length=12, default="General")
    progress_type = models.CharField(choices=PROGRESSTYPE.choices, max_length=12, default="Pending")
    room = models.CharField(max_length=6, default="")

    def same_user(self, newAuthor):
        if self.author != newAuthor:
            return False
        return True
    def check_archived(self):
        if self.progress_type == 'Archived':
            return True
        return False
    def check_active(self):
        if self.progress_type == 'Active':
            return True
        return False
    def check_pending(self):
        if self.progress_type == 'Pending':
            return True
        return False
    def get_progress(self):
        return self.progress_type
    def get_absolute_url(self):
        return reverse("home",kwargs={'pk':self.pk})
    def __str__(self):
        return str(self.author)

class Rooms(models.Model):
    slug = models.SlugField(null=True)
    room_id = models.CharField(max_length=6,default=id_generator(), primary_key=True)
    user = models.CharField(max_length=20, default="")
    specialist = models.CharField(max_length=20, default="")
    active = models.BooleanField(default=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    def is_active(self):
        return active
