from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from customuser.forms import NewMessageForm


def index(request):
    allFaqFirst = Faq.objects.filter(is_first=True)
    allFaqSecond = Faq.objects.filter(is_first=False)
    pageTitle = 'UGS | КЭШБЭК СЕРВИС В СТАВКАХ НА СПОРТ'
    pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
    return render(request, 'pages/index.html', locals())

def about(request):
    pageTitle = 'UGS | О системе | КЭШБЭК СЕРВИС В СТАВКАХ НА СПОРТ'
    pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
    allFeedbacks = Feedback.objects.all()
    return render(request, 'pages/about.html', locals())

def contacts(request):
    pageTitle = 'UGS | Контакты | КЭШБЭК СЕРВИС В СТАВКАХ НА СПОРТ'
    pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
    allFaqFirst = Faq.objects.filter(is_first=True)
    allFaqSecond = Faq.objects.filter(is_first=False)
    form = NewMessageForm()
    return render(request, 'pages/contacts.html', locals())

def robots(request):
    robotsTxt = f"User-agent: *\nDisallow: /admin/\nHost: https://ugscash.ru/\nSitemap: https://ugscash.ru/sitemap.xml"
    return HttpResponse(robotsTxt, content_type="text/plain")

def customhandler404(request, exception, template_name='404.html'):
    pageTitle = 'UGS | Ошибка 404 | КЭШБЭК СЕРВИС В СТАВКАХ НА СПОРТ'
    pageDescription = 'Сервис создан для игроков, которые любят и будут рисковать. UGS - финансовая подушка для игроков, которые привыкли играть на крупные суммы'
    return render(request, 'pages/404.html', None,None,status=404)