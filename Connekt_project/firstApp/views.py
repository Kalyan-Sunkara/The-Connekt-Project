from django.shortcuts import render, redirect, get_object_or_404
from firstApp.forms import UserForm, UserProfileInfoForm, QuestionForm, MessageForm
from firstApp.models import Question, UserProfileInfo, Rooms, Messages

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import QuestionSerializer, MessagesSerializer
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

#API METHOD TO LOAD MESSAGES INTO CHAT ROOM
@api_view(['GET'])
def MessagesForRoom(request,slug):
    # room = request.GET.get('room',None)
    try:
        main_room=get_object_or_404(Rooms,room_id=slug)
        if main_room.user != request.user.username and main_room.specialist.username != request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        messages = Messages.objects.filter(room=main_room)
        serializer = MessagesSerializer(messages, many=True)
        return Response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

#API METHOD TO CREATE MESSAGES IN DATABASE/ makes sure only user can do the request
@api_view(['POST'])
@login_required
def createMessageAPI(request,slug):
    room = request.POST.get('room',None)
    text = request.POST.get('text',None)
    try:
        newRoom = get_object_or_404(Rooms,room_id=room)
        if newRoom.user != request.user.username and newRoom.specialist.username != request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            message = Messages()
            message.room = newRoom
            message.text = text
            message.creator=request.user
            message.creator_name=request.user.username
            message.save()
            serializer = MessagesSerializer(message, many=False)
            return Response(serializer.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required
def disputeQuestionAPI(request,pk):
    try:
        question = Question.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    question.dispute()
    question.save()
    serializer = QuestionSerializer(question, many=False)
    return Response(serializer.data)

def default(request):
    try:
        user = get_object_or_404(UserProfileInfo, user=request.user)
        if get_object_or_404(UserProfileInfo, user=request.user).user_type == "Specialist":
            return redirect("/specialist/")
        else:
            return redirect('/user/')
    except:
        return redirect("about/")

class HomeUserViewList(LoginRequiredMixin,ListView):
    login_url = '/about/'
    redirect_field_name = ''
    template_name = 'firstApp/home_list.html'
    context_object_name = 'questions'
    model = Question
    def get_queryset(self):
         if self.request.user.is_authenticated:
             return Question.objects.filter(author=self.request.user)
         else:
             return Question.objects.none()

    def get_context_data(self,**kwargs):
        context = super(HomeUserViewList,self).get_context_data(**kwargs)
        context['form']=QuestionForm()
        context['active_questions']=Question.objects.filter(progress_type= 'Active',author=self.request.user)
        context['pending_questions']=Question.objects.filter(progress_type= 'Pending', author=self.request.user)
        context['archived_questions']=Question.objects.filter(progress_type= 'Archived', author=self.request.user)
        context['disputed_questions']=Question.objects.filter(progress_type= 'Disputed', author=self.request.user)
        return context



class HomeSpecialistListView(LoginRequiredMixin,ListView):
    login_url = '/about/'
    redirect_field_name = ''
    template_name = 'firstApp/specialist_list.html'
    context_object_name = 'questions'
    model = Question
    def get_queryset(self):
         specialist = get_object_or_404(UserProfileInfo,user = self.request.user)
         if self.request.user.is_authenticated:
             questions = Question.objects.filter(field_type=specialist.field)
             return questions.filter(progress_type="Pending")
         else:
             return Question.objects.none()
    def get_context_data(self,**kwargs):
        specialist=get_object_or_404(UserProfileInfo,user=self.request.user)
        context = super(HomeSpecialistListView,self).get_context_data(**kwargs)
        context['active_questions']=Question.objects.filter(progress_type= 'Active',field_type=specialist.field)
        context['pending_questions']=Question.objects.filter(progress_type= 'Pending', field_type=specialist.field)
        context['disputed_questions']=Question.objects.filter(progress_type= 'Disputed', field_type=specialist.field)
        return context



class QuestionDetailView(LoginRequiredMixin,DetailView):
    login_url = 'about/'
    redirect_field_name = 'firstApp/home_list.html'
    template_name = 'firstApp/question_detail.html'
    context_object_name = 'question'
    model = Question
    def get(self, request, pk):
        try:
            profile = get_object_or_404(UserProfileInfo,user=request.user)
            question = get_object_or_404(Question,pk=pk)
            if profile.user_type == 'User' and profile.user != question.author:
                return redirect('/user/')
            elif profile.user_type == 'Specialist':
                return redirect('/specialist/')
            else:
                self.object = self.get_object()
                context = self.get_context_data(object=self.object)
                return self.render_to_response(context)
        except:
            return redirect('/user/')


class QuestionSpecialistDetailView(LoginRequiredMixin, DetailView):
    login_url = '/about/'
    redirect_field_name = ''
    template_name = 'firstApp/specialist_question_detail.html'
    context_object_name = 'question'
    model = Question



@login_required
def create_room(request, pk):
    question = get_object_or_404(Question,pk=pk)
    room = Rooms()
    room.user = question.author.username
    room.specialist = request.user.username
    room.question = question
    room.slug = room.room_id
    room.save()
    question.progress_type = "Active"
    question.room = room.room_id
    question.save()
    return redirect('/specialist/room/{}'.format(room.room_id))

class roomDetailView(UserPassesTestMixin,LoginRequiredMixin,DetailView):
    login_url = '/about/'
    redirect_field_name = ''
    template_name = "firstApp/room.html"
    context_object_name="room"
    model=Rooms
    # def get(self, request, slug):
        # room = get_object_or_404(Rooms,slug=slug)
        # return redirect('/user/room/{}'.format(slug))
    def handle_no_permission(self):
        return redirect('/')

    def test_func(self):
        room_obj = self.get_object()
        return room_obj.valid_user(self.request.user.username)
    def get_context_data(self,**kwargs):
        room_obj = self.get_object()
        specialist_temp = get_object_or_404(User,username=room_obj.specialist)
        regular_temp = get_object_or_404(User,username=room_obj.user)
        specialist = get_object_or_404(UserProfileInfo,user=specialist_temp)
        regular = get_object_or_404(UserProfileInfo,user=regular_temp)
        context = super(roomDetailView,self).get_context_data(**kwargs)
        context['form']=MessageForm()
        context['messages']=Messages.objects.filter(room=context['room'])
        context['regular']=regular
        context['specialist']=specialist
        return context


@login_required
def createMessage(request,slug):
    if request.method == "POST":
        message_form = MessageForm(data=request.POST)

        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.creator = request.user
            message.creator_name=message.creator.username
            message.room = get_object_or_404(Rooms, slug=slug)
            message.save()
            return redirect('/user/room/{}'.format(slug))
        else:
            return redirect('/user/')
    else:
        return redirect('/user/room/<slug:slug>')


@login_required
def archiveQuestion(request, pk):
    question = get_object_or_404(Question,pk=pk)
    if request.user != question.author:
        return redirect('/')
    question.progress_type = 'Archived'
    question.save()
    return redirect('/user/')

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
            return redirect('/user/')
        else:
            return redirect('/user/')
    else:
        return redirect('/user/')


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
