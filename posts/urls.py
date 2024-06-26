from django.urls import path
from . import views

app_name = 'posts'


urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/profile/', views.signup_next, name='redirect'),
    path('my_posts/', views.post_user, name='my_posts'),
    path('post_create/', views.post_create, name='post_create'),
    path('post_delete/<int:pk>/', views.post_delete, name='post_delete'),
    path('search/', views.search, name='search'),
    path('post_edit/<int:pk>/', views.post_edit, name='post_edit'),
    path('post_detail/<int:pk>/', views.post_detail, name='post_detail'),
    path('post_detail/comment/<int:pk>/', views.comments, name='comments'),
    path('post_detail/like/<int:pk>/', views.like, name='like'),
    path('post_detail/<int:post_id>/comment/<int:pk>/delete/', views.delete_comments, name='delete_comments'),
    path('posts/<str:user_post>/', views.post_author, name='post_author'),
    path('follow/<str:user>/', views.follow, name='follow'),
    path('my_follows/', views.follow_list, name='follow_list'),
    path('group/<slug:slug>/', views.group_posts, name='group_posts'),
    path('ban/<str:user>/', views.ban, name='ban'),
    path('ban_error/', views.ban_error, name='ban_error'),
    path('mute/<str:user>/', views.mute, name='mute'),
    path('chat/<str:user2>/', views.chat, name='chat'),
    path('chat/delete/<int:msg_pk>/', views.chat_message_delete, name='chat_message_delete'),
    path('chat_list/', views.chat_list, name='chat_list'),
    path('image_profile/<str:username>/', views.image_profile, name='image_profile')
]
