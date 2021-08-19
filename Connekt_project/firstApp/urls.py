from django.urls import path
from firstApp import views

#TEMPLATE URLs

app_name="firstApp"

urlpatterns = [
    path('',views.default,name="index"),
    path('user/',views.HomeUserViewList.as_view(),name="home"),
    path('specialist/',views.HomeSpecialistListView.as_view(),name="homeSpecialist"),
    path('userQuestions',views.QuestionDetail,name='questionDetail'),
    path('profile/<slug:slug>',views.profileDetails,name="profile"),
    path('makeQuestion',views.makeQuestion,name="makePost"),
    path('archive/<int:pk>',views.archiveQuestion,name="archive"),
    path('about/',views.about,name='about'),
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('register/',views.register, name="register"),
    path('user/<int:pk>',views.QuestionDetailView.as_view(), name="question-detail"),
    path('specialist/<int:pk>',views.QuestionSpecialistDetailView.as_view(), name="question-detail"),
    path('specialist/createRoom/<int:pk>',views.create_room, name="createRoom"),
    path('specialist/room/<slug:slug>',views.roomDetailView.as_view(), name="room"),
    path('user/room/<slug:slug>',views.roomDetailView.as_view(),name="userRoom"),
    # path('user_login/',views.user_login, name="login")
]
