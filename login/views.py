from django.shortcuts import render, HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from login import models
from login import forms
from .models import Article, Topic, Scenery, Shop, LikeRecord, LikeCount, User
from django.http import JsonResponse
from .templatetags import helper, recommend_itemCF


# Create your views here.
# 主页
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    scenery_top10 = helper.get_hot_scenery(10)
    article_list = helper.get_hot_articles('article', 3)
    return render(request, 'login/index.html', {'scenery_top10': scenery_top10, 'article_list': article_list})


# 登录
def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():  # 确保用户名和密码都不为空
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            # 用户名合法性检验
            # 密码长度验证
            # 更多验证
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_pk'] = user.pk
                request.session['user_name'] = user.name
                request.session['user_email'] = user.email
                request.session['user_address'] = user.address
                request.session['user_sex'] = user.sex
                return redirect('/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
    else:
        return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html')


# 注册
def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            address = register_form.cleaned_data.get('address')

            if password1 != password2:
                message = "两次输入密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用户名已经存在！"
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.address = address
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html')


# 登出
def logout(request):
    if not request.session.get('is_login', None):
        # 如果没有登录，就不会运行
        return redirect('/login/')
    request.session.flush()
    return redirect("/login/")


# 搜索
def search(request):
    search_key = request.GET.get('search')
    post_list = Scenery.objects.filter(content__contains=search_key)
    article_list = Article.objects.filter(content__contains=search_key)
    topic_list = Topic.objects.filter(content__contains=search_key)
    return render(request, 'login/search.html',
                  {'post_list': post_list, 'search_key': search_key, 'article_list': article_list,
                   'topic_list': topic_list})


# 个人页面
def profile(request):
    name_key = request.session.get('user_name')
    user = User.objects.get(name=name_key)
    scenery_list = helper.get_user_like_scenery('scenery', user)
    article_list = helper.get_user_like_article('article', user)
    hot_discussion_list = helper.get_user_like_topic('topic', user)
    profile_list = models.User.objects.get(name=name_key)
    return render(request, 'login/profile.html',
                  {'profile_list': profile_list, 'article_list': article_list, 'scenery_list': scenery_list,
                   'hot_discussion_list': hot_discussion_list})


# 精致文章
def article(request):
    article_list = Article.objects.all()
    return render(request, 'login/Article.html', {'article_list': article_list})


# 商店
def buy(request):
    buy_list = Shop.objects.all()
    return render(request, 'login/buy.html', {'buy_list': buy_list})


# 购买详细页面
def buy_detail(request):
    name = request.GET.get('p1')
    buy_look = Shop.objects.get(name=name)
    return render(request, 'login/buy_detail.html', {'buy_look': buy_look})


# 热议话题
def hot_discussion(request):
    theme_name = request.GET.get('p1', default='毕业旅行')
    theme_now = models.Theme.objects.get(type=theme_name)
    theme_list = models.Theme.objects.all()[1:3]
    hot_discussion_list = Topic.objects.filter(type=theme_name)
    return render(request, 'login/Hot_discussion.html',
                  {'hot_discussion_list': hot_discussion_list, 'theme_list': theme_list, 'theme_now': theme_now})


# 评论话题
def comment_discussion(request):
    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            name = comment_form.cleaned_data.get('name')
            content = comment_form.cleaned_data.get('content')
            type = comment_form.cleaned_data.get('type')
            author = request.session.get('user_name')
            user = User.objects.get(name=author)
            img = user.img

            new_topic = models.Topic()
            new_topic.name = name
            new_topic.type = type
            new_topic.content = content
            new_topic.img = img
            new_topic.author = author
            new_topic.save()

            return redirect('/hot_discussion/')


# 推荐页
def recommend(request):
    name_key = request.session.get('user_name')
    user = User.objects.get(name=name_key)
    recommend_scenery_list = recommend_itemCF.recommend_scenery(user, 4)
    recommend_article_list = recommend_itemCF.recommend_article(user, 4)
    return render(request, 'login/recommend.html',
                  {'recommend_scenery_list': recommend_scenery_list, 'recommend_article_list': recommend_article_list})


# 景区推荐详细页
def recommend_scenery(request):
    name_key = request.session.get('user_name')
    user = User.objects.get(name=name_key)
    recommend_scenery_list = recommend_itemCF.recommend_scenery(user, 12)
    return render(request, 'login/recommend_scenery.html', {'recommend_scenery_list': recommend_scenery_list})


# 文章推荐详细页
def recommend_article(request):
    name_key = request.session.get('user_name')
    user = User.objects.get(name=name_key)
    recommend_article_list = recommend_itemCF.recommend_article(user, 12)
    return render(request, 'login/recommend_article.html', {'recommend_article_list': recommend_article_list})


# 文章详细页
def book(request):
    name = request.GET.get('p1')
    book_list = Article.objects.get(name=name)
    user_name = request.session.get('user_name')
    user = User.objects.get(name=user_name)
    content_type = ContentType.objects.get(model="article")
    read_count, created = models.ReadCount.objects.get_or_create(content_type=content_type, object_id=book_list.id)
    if not request.COOKIES.get('book_%s_%s_read' % (user.id, book_list.pk)):
        # 阅读数量加1
        read_count.read_num += 1
        read_count.save()
        # 创建阅读记录
        new_read_record = models.ReadRecord()
        new_read_record.content_type = content_type
        new_read_record.object_id = book_list.pk
        new_read_record.read_user = user
        new_read_record.save()

    response = render(request, 'login/book.html', {'book_list': book_list, 'read_count': read_count})
    response.set_cookie('book_%s_%s_read' % (user.id, book_list.pk), 'true', max_age=60)
    return response


# 景区详细页
def scenery_look(request):
    name = request.GET.get('p1')
    scenery_message = Scenery.objects.get(name=name)
    user_name = request.session.get('user_name')
    user = User.objects.get(name=user_name)
    content_type = ContentType.objects.get(model="scenery")
    read_count, created = models.ReadCount.objects.get_or_create(content_type=content_type,
                                                                 object_id=scenery_message.id)
    if not request.COOKIES.get('scenery_%s_%s_read' % (user.id, scenery_message.pk)):
        # 阅读数量加1
        read_count.read_num += 1
        read_count.save()
        # 创建阅读记录
        new_read_record = models.ReadRecord()
        new_read_record.content_type = content_type
        new_read_record.object_id = scenery_message.pk
        new_read_record.read_user = user
        new_read_record.save()

    response = render(request, 'login/scenery_look.html',
                      {'scenery_message': scenery_message, 'read_count': read_count})
    response.set_cookie('scenery_%s_%s_read' % (user.id, scenery_message.pk), 'true', max_age=60)
    return response


# 景区页面
def scenery(request):
    scenery_list = Scenery.objects.all()
    return render(request, 'login/scenery.html', {'scenery_list': scenery_list})


# 数据操作成功返回数据方法
def success_response(like_num):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_num'] = like_num
    return JsonResponse(data)


# 数据操作失败返回信息的方法
def error_response(message):
    data = {}
    data['status'] = 'ERROR'
    data['message'] = message
    return JsonResponse(data)


# 点赞（喜欢）
def like_up(request):
    # 得到GET中的数据以及当前用户
    user_name = request.session.get('user_name')
    user = User.objects.get(name=user_name)
    content_type = request.GET.get('content_type')
    content_type = ContentType.objects.get(model=content_type)
    object_id = request.GET.get('object_id')
    is_like = request.GET.get('is_like')

    # 创建一个点赞记录
    if is_like == 'true':
        # 进行点赞，即实例化一个点赞记录
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id,
                                                                like_user=user)
        # 通过created来判断点赞记录是否存在，如果存在则不进行点赞，如果不存在则进行点赞数量加一
        if created:
            # 不存在点赞记录并且已经创建点赞记录，需要将点赞数量加一
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return success_response(like_count.like_num)
        else:
            # 已经进行过点赞
            return error_response('已经点赞过')
    else:
        # 取消点赞
        # 先查询数据是否存在，存在则进行取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, like_user=user).exists():
            # 数据存在，取消点赞
            # 删除点赞记录
            LikeRecord.objects.get(content_type=content_type, object_id=object_id, like_user=user).delete()
            # 判断对应的点赞数量数据是否存在，如果存在则对点赞数量进行减一
            like_count, create = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if create:
                # 数据不存在，返回错误信息
                return error_response('数据不存在，不能取消点赞')
            else:
                # 数据存在，对数量进行减一
                like_count.like_num -= 1
                like_count.save()
                return success_response(like_count.like_num)
        else:
            # 数据不存在，不能取消点赞
            return error_response('数据不存在，不能取消点赞')


# 个性化信息填写
def personality(request):
    if request.method == 'POST':
        personality_list = forms.PersonalityForm(request.POST)
        if personality_list.is_valid():
            problem_one = personality_list.cleaned_data.get('problem_one')
            problem_two = personality_list.cleaned_data.get('problem_two')
            problem_three = personality_list.cleaned_data.get('problem_three')
            user_name = request.session.get('user_name')
            per_user = User.objects.get(name=user_name)

            new_personality = models.Personality()
            new_personality.per_user = per_user
            new_personality.problem_one = problem_one
            new_personality.problem_two = problem_two
            new_personality.problem_three = problem_three
            new_personality.save()

            return redirect('/index/')
