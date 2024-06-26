from django.contrib import admin
from .models import *

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'user', 'group', 'date', 'pk')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'date', 'post')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class BanAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason', 'pk')


class MuteAdmin(admin.ModelAdmin):
    list_display = ('user', 'reason', 'pk')


class ChatAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'message', 'date')


class ChatListAdmin(admin.ModelAdmin):
    list_display = ('chat_user1', 'chat_user2')


class ImgAdmin(admin.ModelAdmin):
    list_display = ('username', 'image')


class RankAdmin(admin.ModelAdmin):
    list_display = ('username', 'rank', 'date', 'rank_img')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Ban, BanAdmin)
admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatList, ChatListAdmin)
admin.site.register(Mute, MuteAdmin)
admin.site.register(ImageProfile, ImgAdmin)
admin.site.register(Rank, RankAdmin)
