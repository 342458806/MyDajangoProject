import json
import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Post
from django.contrib import auth
from django.db.models import Q


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # 获得用户名
        password = request.POST.get('password')  # 获得密码
        # 验证用户名和密码
        user = auth.authenticate(username=username, password=password)
        if user:
            # 验证用户成功，登录成功
            auth.login(request, user)
            return HttpResponse('welcome to the news agent!')
        else:
            # 验证用户失败，登录失败
            return HttpResponse('log fail!please enter the correct password', status=520)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return HttpResponse('logout successfully')


# 必须登陆后才能使用该功能
@login_required
def post(request):
    if request.method == 'POST':
        # 获取json数据，解析json数组
        body = json.loads(request.body)
        # 定义返回信息
        back_msg = {'code': 201, 'msg': ' post successfully'}
        # 获取客户端的post信息
        headline = body['headline']
        category = body['category']
        region = body['region']
        details = body['details']
        # 获取当前用户
        user = request.user
        # 获取创建时间
        time = datetime.datetime.now()
        date = str(time.day) + '/' + str(time.month) + '/' + str(time.year)

        post = Post()
        post.category = category
        post.headline = headline
        post.region = region
        post.details = details
        post.user = user
        post.date = date
        post.save()

        return JsonResponse(back_msg)


@login_required()
def delete(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        # 获取新闻编号
        newsCode = body['story_key']
        if newsCode:
            # 删除成功
            news = Post.objects.filter(id=newsCode)
            if news:
                Post.objects.filter(id=newsCode).delete()
                back_msg = {'code': 201, 'msg': 'delete successfully'}
                return JsonResponse(back_msg, status=201)
            else:
                back_msg = {'code': 503, 'msg': 'delete failed'}
                return JsonResponse(back_msg, status=503)


def get_story(request):
    if request.method == 'GET':
        # 获取用户端的查询请求
        body = json.loads(request.body)
        story_cat = body['story_cat']
        story_region = body['story_region']
        story_date = body['story_date']
        # 创建数组
        news_list = []
        news = Post.objects.all()
        # 判断input条件
        if story_region != '*':
            news = Post.objects.filter(region=story_region)
        if story_cat != '*':
            news = Post.objects.filter(category=story_cat)
        if story_date != '*':
            news = Post.objects.filter(date=story_date)
        if story_region != '*' and story_cat != '*':
            news = Post.objects.filter(region=story_region, category=story_cat)
        if story_region != '*' and story_date != '*':
            news = Post.objects.filter(region=story_region, date=story_date)
        if story_cat != '*' and story_date != '*':
            news = Post.objects.filter(category=story_cat, date=story_date)
        if story_cat != '*' and story_date != '*' and story_region != '*':
            news = Post.objects.filter(region=story_region, category=story_cat, date=story_date)
        # 返回json数组
        if news:
            for new in news:
                new_list = {'key': new.id, 'headline': new.headline, 'story_cat': new.category,
                            'story_region': new.region, 'author': new.user.username, 'story_date': new.date,
                            'story_details': new.details}
                news_list.append(new_list)
            result = {'stories': news_list}
            return JsonResponse(result)
        else:
            return HttpResponse('can not find any story,please try other search conditions',status=404)
