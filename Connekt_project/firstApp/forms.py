from django import forms
from django.contrib.auth.models import User
from firstApp.models import UserProfileInfo, Question

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email','password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic','user_type')

class QuestionForm(forms.ModelForm):
    class Meta():
        model = Question
        fields = ('title','field_type','text', 'price')
        widgets = {
            'title':forms.TextInput(),
            'text' : forms.Textarea(),
            'price':forms.TextInput(),
            'field_type': forms.Select()
            }
        # exclude = ['author']
