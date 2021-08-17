from django.urls import path
from firstApp import views

#TEMPLATE URLs

app_name="firstApp"

urlpatterns = [
    path('',views.HomeViewList.as_view(),name="home"),
    path('userQuestions',views.QuestionDetail,name='questionDetail'),
    path('profile/<slug:slug>',views.profileDetails,name="profile"),
    path('makeQuestion',views.makeQuestion,name="makePost"),
    path('archive/<int:pk>',views.archiveQuestion,name="archive"),
    path('about/',views.about,name='about'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('register/',views.register, name="register"),
    path('<int:pk>',views.QuestionDetailView.as_view(), name="question-detail"),
    # path('user_login/',views.user_login, name="login")
]
