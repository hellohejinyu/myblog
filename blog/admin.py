# -*- coding:utf-8 -*-
# 操作数据模型
from django.contrib import admin
from models import *


class UserlistAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'userpassword', 'realname', 'sex', 'phone', 'score')
    list_filter = ('score',)
    ordering = ('-id',)
    search_fields = ('username',)

class FriendsAdmin(admin.ModelAdmin):
    list_display = ('master', 'slave')
    list_filter = ('master',)
    ordering = ('-id',)
    search_fields = ('master',)
	
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'times', 'summary', 'author',)
    list_filter = ('times',)
    ordering = ('-id',)
    search_fields = ('title',)

class SortsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('-id',)
    search_fields = ('title',)

class TypesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    ordering = ('-id',)
    search_fields = ('title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article_id',)
    ordering = ('-id',)

class ReplayAdmin(admin.ModelAdmin):
    list_display = ('article_id',)
    ordering = ('-id',)
    search_fields = ('title',)

admin.site.register(Userlist, UserlistAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Sorts, SortsAdmin)
admin.site.register(Types, TypesAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Replay, ReplayAdmin)
admin.site.register(Friends, FriendsAdmin)
