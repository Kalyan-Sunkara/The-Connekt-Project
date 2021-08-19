from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

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
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    price = models.PositiveIntegerField(default=1)
    field_type = models.CharField(choices=FIELDTYPE.choices, max_length=12, default="General")
    progress_type = models.CharField(choices=PROGRESSTYPE.choices, max_length=12, default="Pending")

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
