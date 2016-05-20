# -*- coding:utf-8 -*-
from django.db import models
# Create your models here.
IS_SEX = (
    (1, '男'),
    (0, '女'),
    (2, '未知'),
)


class Userlist(models.Model):
    username = models.CharField('用户名', max_length=100)
    userpassword = models.CharField('用户密码', max_length=100)
    email = models.CharField('email', null=True, max_length=100, blank=True)
    realname = models.CharField(
        '真实姓名', max_length=100, null=True, default='匿名')
    sex = models.IntegerField('性别', default=2, choices=IS_SEX)
    phone = models.CharField('电话', null=True, max_length=100, blank=True)
    score = models.IntegerField('人气值', default=0)

    class Meta:
        db_table = 'Userlist'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['score']

    def __unicode__(self):
        return "%s" % self.username

class Friends(models.Model):
	master = models.ForeignKey(Userlist, related_name='master_relate', verbose_name='博主')
	slave = models.ForeignKey(Userlist, related_name='slave_relate', verbose_name='粉丝')

	class Meta:
		db_table = 'Friends'
		verbose_name = '朋友'
		verbose_name_plural = '朋友'
		ordering = ['id']

	def __unicode__(self):
		return "%s->%s" % (self.master, self.slave) 


class Types(models.Model):
    title = models.CharField('大类标题', max_length=20)

    class Meta:
        db_table = 'Types'
        verbose_name = '大类'
        verbose_name_plural = '大类'
        ordering = ['id']

    def __unicode__(self):
        return "%s" % self.title


class Sorts(models.Model):
    title = models.CharField('子类名称', max_length=20)
    type_id = models.ForeignKey(Types, verbose_name='所属大类')
    user_id = models.ForeignKey(Userlist, verbose_name='所属作者')

    class Meta:
        db_table = 'Sorts'
        verbose_name = '子类'
        verbose_name_plural = '子类'
        ordering = ['id']

    def __unicode__(self):
        return "%s" % self.title


class Article(models.Model):
    title = models.CharField('标题', max_length=20)
    summary = models.TextField('摘要',)
    content = models.TextField('内容',)
    times = models.DateTimeField('时间', blank=True)
    sort_id = models.ForeignKey(Sorts, verbose_name='所属子类')
    author = models.ForeignKey(Userlist, verbose_name='作者')
    is_public = models.IntegerField('是否所有人可见', default=1)
    artscore = models.IntegerField('文章点击量', blank=True)
    types_id = models.ForeignKey(Types, verbose_name='所属大类')

    class Meta:
        db_table = 'Article'

        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['id']

    def __unicode__(self):
        return "%s - %s" % (self.title, self.author)


class Comment(models.Model):
    contents = models.TextField('评论内容',)
    article_id = models.ForeignKey(Article, verbose_name='所属文章')
    user_id = models.ForeignKey(Userlist, verbose_name='所属用户')
    times = models.DateTimeField('时间', blank=True)

    class Meta:
        db_table = 'Review'
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['id']


class Replay(models.Model):
    contents = models.TextField('回复内容',)
    article_id = models.ForeignKey(Article, verbose_name='所属文章')
    user_id = models.ForeignKey(Userlist, verbose_name='所属用户')
    re_id = models.ForeignKey(Comment, verbose_name='所属评论')
    times = models.DateTimeField('时间')

    class Meta:
        db_table = 'Replay'
        verbose_name = '回复'
        verbose_name_plural = '回复'
        ordering = ['id']
