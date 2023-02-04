from django.urls import path
from . import views

app_name = 'louslist'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.search, name='search'),
    path('schedule/', views.schedule, name='schedule'),
    path('submitSearch/', views.submitSearch, name='submitSearch'),
    path('friends/', views.friendPage, name="friendPage"),
    path('add_friend/', views.addFriend, name="add_friend"),
    path('delete_friend/<slug:username>', views.deleteFriend, name="delete_friend"),
    path('cancel_request/<slug:username>', views.cancelRequest, name="cancel_request"),
    path('send_friend_request/<slug:userID>/', views.send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/', views.accept_friend_request, name='accept_friend_request'),
    path('decline_friend_request/<int:requestID>/', views.decline_friend_request, name='decline_friend_request'),
    path('<slug:subject>/', views.course_list, name='course_list'),
    path('schedule/', views.schedule, name='schedule'),
    path('add_class/<int:course_number>/', views.add_class, name='add_class'),
    path('delete_class/<int:course_number>', views.delete_class, name='delete_class'),
    path('friend_schedule/<slug:username>/', views.friend_schedule, name='friend_schedule'),
    path('submitComment/<slug:username>/', views.submitComment, name='submit_comment'),
    path('deleteComment/<slug:username>/', views.deleteComment, name='delete_comment'),
]