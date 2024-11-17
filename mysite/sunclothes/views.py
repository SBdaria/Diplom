from django.shortcuts import render
from .forms import *
from .models import Users, Products, ShoppingCart
from datetime import datetime


def homepage(request):
    context = {
        'namepage': 'homepage',
        'title': 'Интернет-магазин "SunClothes"'
    }
    return render(request, 'mainpages/homepage.html', context)


def about_us(request):
    context = {
        'namepage': 'about',
        'title': 'О нас'
    }
    return render(request, 'mainpages/about_us.html', context)


def info(request):
    context = {
        'namepage': 'info',
        'title': 'Оплата и доставка'
    }
    return render(request, 'mainpages/info.html', context)


def catalog(request):
    context = {
        'namepage': 'catalog',
        'title': 'Каталог'
    }
    return render(request, 'mainpages/catalog.html', context)


def shoes(request):
    shoes = Products.objects.filter(category='shoes')
    context = {
        'namepage': 'shoes',
        'category': 'Кроссовки и кеды',
        'type_cloth': shoes
    }
    return render(request, 'mainpages/catalogpage.html', context)


def hoodies(request):
    hoodies = Products.objects.filter(category='hoodies')
    context = {
        'namepage': 'hoodies',
        'category': 'Худи',
        'type_cloth': hoodies
    }
    return render(request, 'mainpages/catalogpage.html', context)


def tshirts(request):
    tshirts = Products.objects.filter(category='tshirts')
    context = {
        'namepage': 'tshirts',
        'category': 'Футболки',
        'type_cloth': tshirts
    }
    return render(request, 'mainpages/catalogpage.html', context)


def jackets(request):
    jackets = [i for i in Products.objects.filter(category='jackets')]
    context = {
        'namepage': 'jackets',
        'category': 'Куртки',
        'type_cloth': jackets
    }
    return render(request, 'mainpages/catalogpage.html', context)


def jeans(request):
    jeans = Products.objects.filter(category='jeans')
    context = {
        'namepage': 'jeans',
        'category': 'Джинсы',
        'type_cloth': jeans
    }
    return render(request, 'mainpages/catalogpage.html', context)


def registration(request):
    """
    function for registration user and write this information into database
    :return: template of page and message about the process of registration
    """
    users = [i.username for i in Users.objects.all()]
    info = {}
    info['namepage'], info['title'] = 'registration', 'Регистрация'
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            repeat_password = form.cleaned_data['repeat_password']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            birthday = form.cleaned_data['birthday']

            if password != repeat_password:
                info['error'] = 'Пароли не совпадают'
            elif username in users:
                info['error'] = 'Пользователь уже существует'
            else:
                if not phone:
                    Users.objects.create(
                        username=username,
                        password=password,
                        email=email,
                        birthday=birthday
                    )
                else:
                    Users.objects.create(
                        username=username,
                        password=password,
                        email=email,
                        phone=phone,
                        birthday=birthday
                    )
                info['error'] = 'Вы успешно зарегистрированы!'
        else:
            info['error'] = 'Данные введены некорректно'
    else:
        form = UserRegisterForm()
        info['form'] = form
    return render(request, 'personality/registration.html', context=info)


def user_login(request):
    """
    function for authentication user and check this information with using database
    :return: template of page and message about the process of authentication
    """
    users = [i.username for i in Users.objects.all()]
    info = {}
    info['namepage'], info['title'] = 'login', 'Вход в аккаунт'
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if username in users:
                find_user = Users.objects.get(username=username)
                correct_password = find_user.password

                if password == correct_password:
                    context = {
                        'username': find_user.username,
                        'email': find_user.email,
                        'phone': find_user.phone,
                        'birthday': find_user.birthday
                    }
                    return render(request, 'personality/profil.html', context=context)
                else:
                    info['error'] = 'Пароли не совпадают'

            else:
                info['error'] = 'Такой пользователь не зарегистрирован'
        else:
            info['error'] = 'Данные введены некорректно'
    else:
        form = UserAuthenticationForm()
        info['form'] = form
    return render(request, 'personality/login.html', context=info)


def cart_info(request, pk):
    """
    function for make order
    :return: template of page and message about status order
    """
    cloth = Products.objects.get(pk=pk)
    users = [i.username for i in Users.objects.all()]
    context = {
        'namepage': 'details',
        'title': 'Подтверждение заказа',
        'cloth': cloth
    }
    if request.method == 'POST':
        form = UserAuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if username in users:
                find_user = Users.objects.get(username=username)
                correct_password = find_user.password

                if password == correct_password:
                    ShoppingCart.objects.create(
                        user=find_user,
                        product=cloth,
                        date_order=datetime.now().strftime('%Y-%m-%d %H:%M')
                    )
                    info = {
                        'namepage': 'submit_order',
                        'title': 'Ваш заказ успешно подтвержден',
                    }
                    return render(request, 'mainpages/submit_order.html', context=info)
                else:
                    context['error'] = 'Пароли не совпадают'

            else:
                context['error'] = 'Такой пользователь не зарегистрирован'
        else:
            context['error'] = 'Данные введены некорректно'
    else:
        form = UserAuthenticationForm()
        context['form'] = form
    return render(request, 'mainpages/cart_info.html', context=context)
