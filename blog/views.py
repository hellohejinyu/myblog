# Create your views here.
# coding=utf-8
from models import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
import sys
import time
import tests
import random
import hashlib
reload(sys)
sys.setdefaultencoding('utf8')

def ClickFocus(request):
	people = request.session.get('people')
	userDetail = request.session.get('userDetail')

	if people and userDetail:

		id = userDetail.id

		ans = Friends.objects.filter(master=userDetail,slave=people)
		if ans:
			ans.delete()
		else:
			ans = Friends()
			ans.master=userDetail
			ans.slave=people
			ans.save()

		url = '/detail/%d' % id
		return HttpResponseRedirect(url)
	else:
		return HttpResponseRedirect('/login/')

def Detail(request, id):
    userDetail = Userlist.objects.get(id = id)
    request.session['userDetail'] = userDetail
    fansCount = len(Friends.objects.filter(master = userDetail))
    focusCount = len(Friends.objects.filter(slave = userDetail))
    article = Article.objects.filter(author=userDetail, is_public=1).order_by("-id")
    if request.session.get('people') is not None:
        people = request.session.get('people')
        user = Userlist.objects.get(username=people.username)     
        mark = 0
        if user == userDetail:
            mark = -2
        if(Friends.objects.filter(master=userDetail, slave=user)):
            mark = 1
    else:
        mark = -1
        user = ''      

    return render_to_response('detail.html', {'mark':mark, 'people':user, 'userDetail':userDetail, 'articles':article, 'focusC': focusCount, 'fansC': fansCount})


def Focus(request):
    if request.session.get('people') is not None:
        people = request.session.get('people')
        user = Userlist.objects.get(username = people.username)
        focus = Friends.objects.filter(slave = people)
        fans = Friends.objects.filter(master = people)
        focusCount = len(focus)
        fansCount = len(fans)
        return render_to_response('focus.html',{'people': user, 'focus': focus, 'fans':fans, 'focusC': focusCount, 'fansC': fansCount})
    else:
        return HttpResponseRedirect('/login/')

def Test(request):
    return render_to_response('editplus.html')

def About(request):
    people = request.session.get('people')
    return render_to_response('about.html', {'people': people})


def Main(request):
    return HttpResponseRedirect('/index/')


def SearchBlog(request):
    if 's' in request.GET:
        s = request.GET['s']
        # 点击量计算
        artdjl = Article.objects.all().order_by("-artscore")[0:5]
        userdjl = Userlist.objects.all().order_by("-score")[0:5]
        if not s:
            articles = Article.objects.filter(is_public=1).order_by("-id")
            return render_to_response('login.html', {'articles': articles, 'artdjl': artdjl, 'userdjl': userdjl})
        else:
            articles = Article.objects.filter(title__icontains=s, is_public=1)
            return render_to_response('login.html', {'articles': articles, 'artdjl': artdjl, 'userdjl': userdjl})


def TimeLine(request):
    people = request.session.get('people')
    articles = Article.objects.all().order_by("-id")[0:10]
    return render_to_response("timeline.html", {'people': people, 'articles': articles})


def Login(request):
    if request.method == 'GET':
        flag = ''
        if request.session.get('flag') is not None:
            flag = '登录失败！'
            del request.session['flag']
        if request.session.get('people') is not None:
            del request.session['people']
        types = Types.objects.all()
        # 时间排序
        article = Article.objects.filter(is_public=1).order_by("-id")
        # 点击量计算
        artdjl = Article.objects.filter(is_public=1).order_by("-artscore")[0:5]
        userdjl = Userlist.objects.all().order_by("-score")[0:5]

        after_range_num = 4
        befor_range_num = 4
        try:
            page = int(request.GET.get("page", 1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(article, 4)
        try:
            article = paginator.page(page)
        except(Empte, InvalidPage, PageNotAnInteger):
            article = paginator.page(paginator.num_pages)
        if page >= after_range_num:
            page_range = paginator.page_range[
                page - after_range_num:page + befor_range_num]
        else:
            page_range = paginator.page_range[0:int(page) + befor_range_num]

        return render_to_response("login.html", {'types': types, 'articles': article, 'artdjl': artdjl, 'userdjl': userdjl, 'flag': flag})
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        m = hashlib.md5()
        m.update(password)
        password_md5 = m.hexdigest()
        flag = 0
        user = Userlist.objects.filter(
            username=username, userpassword=password_md5)
        if len(user) > 0:
            people = Userlist.objects.get(username=username)
            request.session['people'] = people
            return HttpResponseRedirect('/index/')
        else:
            request.session['flag'] = flag
            return HttpResponseRedirect('/login/')


# 点击右下角大类时的显示内容
def TypesC(request, id):
    if request.session.get('people') is not None:
        if id is None or id == '':
            peo = request.session.get('people', None)
            # article = Article.objects.filter(author=peo)
            article = Article.objects.filter(types_id=id, is_public=1).order_by("-id")
        else:
            peo = request.session.get('people', None)
            # article = Article.objects.filter(author=peo,types_id=id)
            article = Article.objects.filter(types_id=id, is_public=1).order_by("-id")

        sorts = Sorts.objects.filter(user_id=peo.id)
        sortsCount = len(sorts)

        articleMe = Article.objects.filter(author=peo).order_by("-id")
        articlesMeCount = len(articleMe)

        types = Types.objects.all()

        after_range_num = 4
        befor_range_num = 4
        try:
            page = int(request.GET.get("page", 1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(article, 4)
        try:
            article = paginator.page(page)
        except(Empte, InvalidPage, PageNotAnInteger):
            article = paginator.page(paginator.num_pages)
        if page >= after_range_num:
            page_range = paginator.page_range[
                page - after_range_num:page + befor_range_num]
        else:
            page_range = paginator.page_range[0:int(page) + befor_range_num]
        return render_to_response('types.html', {'people': peo, 'articles': article, 'sortsCount': sortsCount, 'articlesMeCount': articlesMeCount, 'types': types})
    else:
        return HttpResponseRedirect('/index/')


# 个人界面点击左边分类，右边文章的显示情况
def SortsC(request, sortid):
    if request.session.get('people') is not None:
        if id is None or id == '':
            peo = request.session.get('people', None)
            article = Article.objects.filter(author=peo)
        else:
            peo = request.session.get('people', None)
            sort = Sorts.objects.get(id=sortid)
            article = Article.objects.filter(author=peo, sort_id=sort)

        sorts = Sorts.objects.filter(user_id=peo.id)
        sortsCount = len(sorts)

        articleMe = Article.objects.filter(author=peo)
        articlesMeCount = len(articleMe)

        fuckSorts = 1

        after_range_num = 4
        befor_range_num = 4
        try:
            page = int(request.GET.get("page", 1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(article, 4)
        try:
            article = paginator.page(page)
        except(Empte, InvalidPage, PageNotAnInteger):
            article = paginator.page(paginator.num_pages)
        if page >= after_range_num:
            page_range = paginator.page_range[
                page - after_range_num:page + befor_range_num]
        else:
            page_range = paginator.page_range[0:int(page) + befor_range_num]
        return render_to_response('types.html', {'fuckSorts': fuckSorts, 'people': peo, 'articles': article, 'sorts': sorts, 'sortsCount': sortsCount, 'articlesMeCount': articlesMeCount})
    else:
        return HttpResponseRedirect('/index/')

# 首页显示，有public和private之分，如果没有登录，则跳转到/login/


def Index(request, value):

    if request.session.get('people') is not None:
        peo = request.session.get('people', None)

        if (value is None or value == '') or value == 'public':
            article = Article.objects.all().filter(is_public=1).order_by("-id")
            articleMe = Article.objects.filter(author=peo).order_by("-id")
            articlesMeCount = len(articleMe)
            types = Types.objects.all()
            sorts = Sorts.objects.filter(user_id=peo.id)
            sortsCount = len(sorts)

            after_range_num = 4
            befor_range_num = 4
            try:
                page = int(request.GET.get("page", 1))
                if page < 1:
                    page = 1
            except ValueError:
                page = 1
            paginator = Paginator(article, 4)
            try:
                article = paginator.page(page)
            except(Empte, InvalidPage, PageNotAnInteger):
                article = paginator.page(paginator.num_pages)
            if page >= after_range_num:
                page_range = paginator.page_range[
                    page - after_range_num:page + befor_range_num]
            else:
                page_range = paginator.page_range[
                    0: int(page) + befor_range_num]

            return render_to_response('index.html', {'people': peo, 'types': types, 'value': value, 'articles': article, 'sortsCount': sortsCount, 'articlesMeCount': articlesMeCount})
        else:

            article = Article.objects.filter(author=peo).order_by("-id")
            articlesMeCount = len(article)
            sorts = Sorts.objects.filter(user_id=peo.id)
            sortsCount = len(sorts)

            after_range_num = 4
            befor_range_num = 4
            try:
                page = int(request.GET.get("page", 1))
                if page < 1:
                    page = 1
            except ValueError:
                page = 1
            paginator = Paginator(article, 4)
            try:
                article = paginator.page(page)
            except(Empte, InvalidPage, PageNotAnInteger):
                article = paginator.page(paginator.num_pages)
            if page >= after_range_num:
                page_range = paginator.page_range[
                    page - after_range_num:page + befor_range_num]
            else:
                page_range = paginator.page_range[
                    0: int(page) + befor_range_num]

            return render_to_response('index.html', {'people': peo, 'sorts': sorts, 'value': value, 'articles': article, 'sortsCount': sortsCount, 'articlesMeCount': articlesMeCount})
    else:
        return HttpResponseRedirect('/login/')

# 提交博文
def Releaseblog(request):
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    if request.session.get('people') != None:
        peo = request.session.get('people',None)
        sorts=Sorts.objects.filter(user_id=peo)
        types=Types.objects.all()
        if request.method == "GET":
            return render_to_response('releaseblog.html',{'people':peo,'sorts':sorts,'types':types}) 
        if request.method == "POST":
            typeid=request.POST.get("type_id")
            sortid=request.POST.get("sort")
            newsort=request.POST.get("newsort")
            ispublic = request.POST.get("ispublic")
            if sortid == "1newsort":
                sort=Sorts()
                sort.title=newsort
                sort.type_id=Types.objects.get(id=typeid)
                sort.user_id=peo
                sort.save()

        biaoti=request.POST.get("biaoti")
        zhaiyao=request.POST.get("zhaiyao")
        neirong=request.POST.get("content")
        if sortid== "1newsort":
            sortid = Sorts.objects.get(title=newsort,user_id=peo).id 
        sort=Sorts.objects.get(id=int(sortid))
        art=Article()
        art.title=biaoti
        art.summary=zhaiyao
        art.content=neirong
        art.times=now
        art.is_public=ispublic
        art.author=peo
        art.artscore=1
        art.sort_id=sort
        art.types_id=sort.type_id
        art.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
 # 注册用户       
def RegisterUser(request):
    if request.method=='GET':
            return render_to_response('user/info.html')
    if request.method=='POST':
        name=request.POST.get("username")
        password = request.POST.get('password')
        m = hashlib.md5()
        m.update(password)
        password_md5 = m.hexdigest()
        users =Userlist.objects.filter(username=name)
        if len(users)<=0:
            validateNum = '1'
            user=Userlist()
            user.username=name
            user.userpassword=password_md5
            request.session['validateNum'] = validateNum
            request.session['user'] = user
            return HttpResponseRedirect('/checkregister/')
        else:
            validateNum = '0'
            request.session['validateNum'] = validateNum
            return HttpResponseRedirect('/checkregister/') 
 # 验证注册
def CheckRegister(request):
    try:
        if request.session['user']:
            yanzhengma = '1'
            user=request.session['user']
            yanzhengcheck=request.session['validateNum']
            if yanzhengma == yanzhengcheck:
                del request.session['user']
                del request.session['validateNum']
                user.save()
                return render_to_response('user/success.html')
            else:
                return render_to_response('user/fail.html')
    except Exception, e:
        return render_to_response('user/fail.html')

# 打开博客界面       
def ReadBlog(request,id):
    people = request.session.get('people')
    article = Article.objects.get(id=int(id))
    ispublic = article.is_public
    author = article.author
    if (ispublic == 0 and author == people) or ispublic == 1:
        user = Userlist.objects.get(username=article.author)
        newUserScore = user.score+1
        user.score = newUserScore
        user.save()
        newscore=article.artscore+1
        article.artscore=newscore
        article.save()
        type_this = Types.objects.get(title=article.types_id)
        hostAddr = request.get_host() 
        return render_to_response('readblog.html',{'people':people, 'hostAddr':hostAddr, 'articles':article,'type':type_this})
    else:
        return render_to_response('noauthority.html', {'people':people, 'articles':article})

def EditInfo(request):
    if request.session.get('people') != None: 
        peo = request.session.get('people')
        username=peo.username
        user=Userlist.objects.get(username=username)
        if request.method == "GET":
            return render_to_response('edit.html',{'people':user}) 
    else:
        return HttpResponseRedirect('/login/') 

def EditPlus(request):
    if request.session.get('people') is not None:
        peo = request.session.get('people')
        username=peo.username
        user=Userlist.objects.get(username=username)
        if request.method == "GET":
            return HttpResponseRedirect('/edit',{'people':user})
        if request.method == "POST":
            realname=request.POST.get("realname")
            email=request.POST.get("email")
            phone=request.POST.get("phone")
            user.realname = realname
            user.email = email
            user.phone = phone
            user.save()
            markEdit = '修改成功！'
            return render_to_response('edit.html', {'people':user, 'markEdit': markEdit})
    else:
        return HttpResponseRedirect('/login/')

def ChangePas(request):
    if request.session.get('people') is not None:
        peo = request.session.get('people')
        username = peo.username
        user = Userlist.objects.get(username = username)
        if request.method == 'GET':
            return HttpResponseRedirect('/edit', {'people': user})
        if request.method == 'POST':
            newpas = request.POST.get("newpas")
            m = hashlib.md5()
            m.update(newpas)
            password_md5 = m.hexdigest()
            user.userpassword = password_md5
            user.save()
            markEdit = '密码修改成功，建议重新登录！'
            linkLogin = '1'
            return render_to_response('edit.html', {'people':user, 'markPas': markEdit, 'linkLogin': linkLogin})
    else:
        return HttpResponseRedirect('/login/')        

def EditBlog(request):
    people = request.session.get('people')
    article = Article.objects.filter(author=people).order_by("-id")
    return render_to_response("editblog.html",{'people':people, 'articles':article})    
    
def DelArticle(request,id):
    people = request.session.get('people')
    article = Article.objects.filter(author=people,id=id)
    article.delete()
    return HttpResponseRedirect('/editblog/')

def ChangeBlog(request,id):
    people = request.session.get('people')
    article = Article.objects.filter(author=people,id=id)
