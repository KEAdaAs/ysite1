import random

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from rstie.models import Poem, abzats


def otziv_read(request):
    if not request.user.is_authenticated:
        return redirect('/login')


def otziv(request):
    if not request.user.is_authenticated:
        return redirect('/login')


def index(request):
    # если мы залогинены
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, "index.html")


def login_page(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')

        if username == '' or password == '':
            return HttpResponse("Заполните все поля")

        # проверяем правильность логина и пароля
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse("Логин неверен")


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('login', '')
        password = request.POST.get('password', '')
        email = request.POST.get('email', '')

        if username == '' or password == '' or email == '':
            return HttpResponse("Заполните все поля")

        if User.objects.filter(username=username).exists():
            return HttpResponse("Логин занят")

        # создаем пользователя
        user = User.objects.create_user(username, email, password)
        user.save()

        # "входим" пользователя
        login(request, user)

        return redirect('/')


def logout_page(request):
    if request.method == 'POST':
        logout(request)
    return redirect('/login')


def maiin(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'main_page.html')


def read(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    poems = Poem.objects.filter(ended=True)
    if poems.count() == 0:
        return HttpResponse("Пока еще нет готовых.")
    if "id" not in request.GET:
        poem = random.choice(poems)
    else:
        poem = Poem.objects.get(pk=request.GET['id'])
    paragraphs = abzats.objects.filter(poem=poem)
    return render(request, 'reading.html', {'poems': poems, 'poem': poem, 'paragraphs': paragraphs})


def write(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        poems = Poem.objects.filter(ended=False)
        if poems.count() == 0:
            return HttpResponse("Пока еще нет начатых.")
        else:
            poem = random.choice(poems)

        abzats1 = abzats.objects.filter(poem=poem)
        return render(request, 'shablon.html', {'poem': poem, 'abzats' : abzats1})

    if request.method == 'POST':
        id = request.POST['id']
        text = request.POST['write']
        poem = Poem.objects.get(pk=id)

        if "button" in request.POST:
            poem.ended = True

        poem.save()
        current_user = request.user
        record = abzats()
        record.poem = poem
        record.text = text
        record.user = current_user
        record.save()
        abzats1 = abzats.objects.filter(poem=poem)
        return render(request, 'shablon.html', {'poem': poem, 'abzats' : abzats1})


def creating(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        return render(request, 'creating_poem.html')

    if request.method == 'POST':
        text = request.POST['create']
        name = request.POST['create1']
        poem = Poem()
        poem.text = ""
        poem.name = name

        paragraph = abzats()
        paragraph.text = text
        paragraph.user = request.user
        if "button2" in request.POST:
            pass
        else:
            poem.ended = False

        poem.save()
        paragraph.poem = poem
        paragraph.save()
        abzats1 = abzats.objects.filter(poem=poem)
        return render(request, 'creating_poem.html', {'poem': poem, 'abzats' : abzats1})
