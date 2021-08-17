from django.shortcuts import render, redirect, get_object_or_404
from firstApp.forms import UserForm, UserProfileInfoForm, QuestionForm
from firstApp.models import Question, UserProfileInfo

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer
# from . import forms
# from firstApp.forms import NewUserForm
# from firstApp.forms import CreateUserForm
# from django.contrib.auth.forms import UserCreationForm
UserModel = get_user_model()

# @api_view(['GET'])
# def QuestionList(request):
#     questions = Question.objects.all()
#     serializer = QuestionSerializer(questions, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def QuestionDetail(request):
    questions = Question.objects.filter(author=request.user)
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)

class HomeViewList(LoginRequiredMixin,ListView):
    login_url = 'about/'
    redirect_field_name = 'firstApp/home_list.html'
    template_name = 'firstApp/home_list.html'
    context_object_name = 'questions'
    model = Question
    def get_queryset(self):
         if self.request.user.is_authenticated:
             return Question.objects.filter(author=self.request.user)
         else:
             return Question.objects.none()
    def get_context_data(self,**kwargs):
        context = super(HomeViewList,self).get_context_data(**kwargs)
        context['form']=QuestionForm()
        context['active_questions']=Question.objects.filter(progress_type= 'Active',author=self.request.user)
        context['pending_questions']=Question.objects.filter(progress_type= 'Pending', author=self.request.user)
        context['archived_questions']=Question.objects.filter(progress_type= 'Archived', author=self.request.user)
        return context
class QuestionDetailView(LoginRequiredMixin,DetailView):
    login_url = 'about/'
    redirect_field_name = 'firstApp/home_list.html'
    template_name = 'firstApp/question_detail.html'
    context_object_name = 'question'
    model = Question
@login_required
def archiveQuestion(request, pk):
    question = get_object_or_404(Question,pk=pk)
    question.progress_type = 'Archived'
    question.save()
    return redirect('/')
@login_required
def profileDetails(request, slug):
    if request.user.username == slug:
        if request.user.username == 'kalyan':
            profile = request.user
            return render(request, 'firstApp/profile_detail.html', {'profile': profile})
        profile = get_object_or_404(UserProfileInfo,user=request.user)
        return render(request, 'firstApp/profile_detail.html', {'profile': profile})
    else:
        return redirect('/')

@login_required
def makeQuestion(request):
    if request.method == "POST":
        question_form = QuestionForm(data=request.POST)

        if question_form.is_valid():
            # print(question.id_author)
            # print(question.author)
            question = question_form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('/')
        else:
            return redirect('/')
    else:
        return redirect('/')
def about(request):
    return render(request, 'firstApp/about.html')

def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.is_active = False
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.slug = '{}'.format(profile.user)

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            # registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'registration/register.html',
                                {'user_form':user_form,
                                    'profile_form':profile_form,
                                    'registered':registered})

# Create your views here.
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
