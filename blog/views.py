from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import *

def posts(request):
    rel_link = 'https://ugscash.ru/blog/'
    all_posts = BlogPost.objects.filter(is_active=True).order_by('-created_at')
    all_filters = BlogCategory.objects.all()
    pageTitle = 'UGS | Блог | КЭШБЭК СЕРВИС В СТАВКАХ НА СПОРТ'
    pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
    return render(request, 'blog/posts.html', locals())


def post(request,article_name_slug):

    if request.POST:
        if request.POST.get('c_id') == '':
            BlogComment.objects.create(category_id=request.POST.get('p_id'),
                                       user_id=request.POST.get('u_id'),
                                       text=request.POST.get('text'))
        else:
            BlogCommentComment.objects.create(comment_id=request.POST.get('c_id'),
                                              user_id=request.POST.get('u_id'),
                                              text=request.POST.get('text'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    print(article_name_slug)
    if article_name_slug == 'ttt':
        return HttpResponseRedirect('/')
    else:
        post = get_object_or_404(BlogPost, name_slug=article_name_slug)

        pageTitle = post.title
        pageDescription = post.description
        allComments = BlogComment.objects.filter(category=post)
        rel_link = f'https://ugscash.ru/blog/{post.name_slug}'

        try:
            mostLike = BlogPost.objects.filter(is_active=True).order_by('-created_at')[0:3]

        except:
            mostLike = None
        return render(request, 'blog/post.html', locals())
