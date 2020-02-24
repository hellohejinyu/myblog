# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
# from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# from django.contrib import auth
# 容许用户有权限管理所建立站点，否则不能
admin.autodiscover()

urlpatterns = patterns(
  '',
  # Examples:
  # Uncomment the admin/doc line below to enable admin documentation:
  # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
  # Uncomment the next line to enable the admin:
  url(r'^$', 'blog.views.Main'),
  url(r'^admin/', include(admin.site.urls)),
  url(r'^register/$', 'blog.views.RegisterUser'),
  url(r'^checkregister/$', 'blog.views.CheckRegister'),
  url(r'^login/$', 'blog.views.Login'),
  url(r'^release/$', 'blog.views.Releaseblog'),
  url(r'^index/(.*)$', 'blog.views.Index'),
  url(r'^blogs/(.*)$', 'blog.views.ReadBlog'),
  url(r'^delete/(.*)$', 'blog.views.DelArticle'),
  url(r'^types/(.*)$', 'blog.views.TypesC'),
  url(r'^sorts/(.*)$', 'blog.views.SortsC'),
  url(r'^timeline/$', 'blog.views.TimeLine'),
  url(r'^search/$', 'blog.views.SearchBlog'),
  url(r'^edit/$', 'blog.views.EditInfo'),
  url(r'^about/$', 'blog.views.About'),
  url(r'^editblog/$', 'blog.views.EditBlog'),
  url(r'^friends/$', 'blog.views.Focus'),
  url(r'^editplus/$', 'blog.views.EditPlus'),
  url(r'^changepas/$', 'blog.views.ChangePas'),
  url(r'^detail/(.*)$', 'blog.views.Detail'),
  url(r'^clickfocus/$', 'blog.views.ClickFocus'),
)
