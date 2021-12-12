"""
Definition of views.
"""

from typing import Any
from django.contrib.auth.models import User
from django.db.models import query
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

import types

from django.db.models import Value

from django.contrib.auth.forms import UserCreationForm

from app.forms import AddAlbumForm, AddImagesForm, AddProductForm, CommentForm, EditUserForm

from .models import Album, Cart, Client, Comment, Images, News, Order, Product, Status, Categories

import random

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'year':datetime.now().year,
        }
    )

def news(request):
    """Renders the about page."""
    news = News.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/news.html',
        {
            'news' : news,
            'title':'Новости',
            'year':datetime.now().year,
        }
    )

def news_post(request, parametr):
    print('\n\n\IM HERE!!!!!!!!!!!!!!\n\n')
    post = News.objects.get(id = parametr)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/news_post.html',
        {
            'post' : post,
            'title':'Новости',
            'year':datetime.now().year,
        }
    )

def catalog(request):

    q = '''
    select
    p.id,
    p.name as productName,
    p.product_id as productCode,
    p.description_short as productDescriptionShort,
    p.description_full as productDescriptionFull,
    p.price as productPrice
    from Products as p
    join Categories as c
    on p.category_id = c.id
    order by c.name, productPrice
    '''

    products_tmp = Product.objects.raw(q)

    class Product_tmp:
        def __init__(self, product, images):
            self.productID = product.id
            self.productCode = product.productCode
            self.productName = product.productName
            self.productDescriptionShort = product.productDescriptionShort
            self.productDescriptionFull = product.productDescriptionFull
            self.productPrice = product.productPrice
            self.productImages = []
            for img in images:
                self.productImages.append(str(img.img.url))
            self.productImage = self.productImages[0]

    products = []

    for product in products_tmp:
        images = Images.objects.filter(album_id = product.album_id)
        products.append(Product_tmp(product, images))

    categories = Categories.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/catalog.html',
        {
            'title': 'Каталог',
            'categories': categories,
            'products': products,
            'year':datetime.now().year,
            }
        )

def catergory(request, parametr):
    q = '''
    select
    p.id,
    p.name as productName,
    p.product_id as productCode,
    p.description_short as productDescriptionShort,
    p.description_full as productDescriptionFull,
    p.price as productPrice
    from Products as p
    join Categories as c
    on c.id = p.category_id
    ''' + 'where c.id = ' + str(parametr) + ' order by productPrice'

    products_tmp = Product.objects.raw(q)

    class Product_tmp:
        def __init__(self, product, images):
            self.productID = product.id
            self.productCode = product.productCode
            self.productName = product.productName
            self.productDescriptionShort = product.productDescriptionShort
            self.productDescriptionFull = product.productDescriptionFull
            self.productPrice = product.productPrice
            self.productImages = []
            for img in images:
                self.productImages.append(str(img.img.url))
            self.productImage = self.productImages[0]

    products = []

    for product in products_tmp:
        images = Images.objects.filter(album_id = product.album_id)
        products.append(Product_tmp(product, images))

    categories = Categories.objects.all()

    # products = Product.objects.raw(query)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/catalog.html',
        {
            'title': 'Каталог',
            'products': products,
            'categories': categories,
            'year':datetime.now().year,
            }
        )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            Client.objects.create(username = reg_f.username, user = User.objects.get(username = reg_f.username))
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def product(request, parametr):
    q = '''
    select
    p.id,
    p.name as productName,
    p.product_id as productCode,
    p.description_short as productDescriptionShort,
    p.description_full as productDescriptionFull,
    p.price as productPrice
    from Products as p
    where productCode = 
    ''' + str(parametr)

    products_tmp = Product.objects.raw(q)

    class Product_tmp:
        def __init__(self, product, images):
            self.productID = product.id
            self.productCode = product.productCode
            self.productName = product.productName
            self.productDescriptionShort = product.productDescriptionShort
            self.productDescriptionFull = product.productDescriptionFull
            self.productPrice = product.productPrice
            self.productImages = []
            for img in images:
                self.productImages.append(str(img.img.url))
            self.productImage = self.productImages[0]

    products = []

    for product in products_tmp:
        images = Images.objects.filter(album_id = product.album_id)
        products.append(Product_tmp(product, images))

    try:
        comments = Comment.objects.filter(product = product)
    except Comment.DoesNotExist:
        comments = None

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit = False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.product = Product.objects.get(product_id = parametr)
            comment_f.save()

            return redirect('product', parametr = product.product_id)
    else: 
        form = CommentForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/product.html',
        {
            'product': products[0],
            'comments': comments,
            'form': form,
            'title':'Продукт',
            'year':datetime.now().year,
        }
    )

def managerOrders(request):

    querySum = '''select 
    o.id,
    o.client_id as clientID,
    o.order_id as orderID,
    o.date as orderDate,
    sum(p.price) as totalSum,
    s.text as orderStatus,
    s.colorHEX as statusColor
    from Products as p
    join Orders as o
    on o.product_id = p.id
    join Statuses as s
    on o.status_id = s.id 
    group by o.order_id 
    order by s.id, o.date'''

    qOrders = '''
    select
    o.id,
    o.client_id as clientID,
    o.order_id as orderID,
    p.id as prdoductID,
    p.product_id as productCode,
    p.name as productName,
    p.price as productPrice,
    p.album_id as productAlbum,
    count(p.id) as productCount,
    sum(p.price) as sumForCount
    from Orders as o
    join Products as p
    on o.product_id = p.id
    group by p.id, o.order_id'''

    orders_tmp = Order.objects.raw(qOrders)
    # Нужные поля объекта:
    # orderID - номер заказа
    # clientID - id клиента (из таблицы заказов) ? мб не нужно
    # productID - id продукта (pdoduct_id из Product, не id из таблицы)
    # productName - имя продукта
    # productPrice - цена за единицу
    # countOfProduct - количество
    # sumForCount - цена за все количество одного продукта

    class Order_tmp:
        def __init__(self, product, images):
            self.orderID = product.orderID
            self.productID = product.id
            self.productCode = product.productCode
            self.productName = product.productName[:40]
            self.productPrice = product.productPrice
            self.productCount = product.productCount
            self.sumForCount = product.sumForCount
            # self.orderDate = product.orderDate
            self.productImages = []
            for img in images:
                self.productImages.append(str(img.img.url))
            self.productImage = self.productImages[0]

    orders = []

    for order in orders_tmp:
        images = Images.objects.filter(album_id = order.productAlbum)
        print('\n-\n', images.query, '\n-\n')
        orders.append(Order_tmp(order, images))

    sums = Order.objects.raw(querySum)
    # Нужные поля объекта:
    # clientID - id клиента
    # orderID - номер заказа
    # totalSum - общая сумма заказа

    # Есть ли способ лучше написать запросы к бд?..

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/manager-orders.html',
        {
            'sums': sums,
            'orders': orders,
            'title':'Заказы',
            'year':datetime.now().year,
        }
    )

def clientCart(request):

    qCart = '''
    select
    c.id,
    c.product_id,
    p.id as productID,
    p.name as productName,
    p.price as productPrice,
    p.product_id as productCode,
    p.album_id as productAlbum,
    sum(p.price) as sumForCount,
    count(p.id) as productCount
    from Carts as c
    join Products as p
    on p.id = c.product_id
    where c.client_id = 
    ''' + str(request.user.id) + ' group by productID'

    carts_tmp = Cart.objects.raw(qCart)

    class Cart_tmp:
        def __init__(self, product, images):
            self.cartID = product.id
            self.productID = product.productID
            self.productCode = product.productCode
            self.productName = product.productName[:40]
            self.productPrice = product.productPrice
            self.productCount = product.productCount
            self.sumForCount = product.sumForCount
            self.productImages = []
            for img in images:
                self.productImages.append(str(img.img.url))

    products = []

    for cart in carts_tmp:
        images = Images.objects.filter(album_id = cart.productAlbum)
        print('\n-\n', images.query, '\n-\n')
        products.append(Cart_tmp(cart, images))

    totalSum = 0
    for cart in products:
        totalSum += cart.productPrice * cart.productCount

    profileFilled = False
    client = Client.objects.get(username = request.user.username)
    if client.first_name and client.last_name and client.phone and client.email:
        profileFilled = True

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/client-cart.html',
        {
            'profileFilled': profileFilled,
            'totalSum': totalSum,
            'products': products,
            'title':'Корзина',
            'year':datetime.now().year,
        }
    )

def addToCart(request, parametr):
    product = Product.objects.get(id = parametr)
    client = User.objects.get(id = request.user.id)
    Cart.objects.create(product = product, client = client)

    return redirect('client-cart')

def removeFromCart(request, parametr):
    cart = Cart.objects.get(id = parametr)
    cart.delete()

    return redirect('client-cart')

def makeOrders(request, parametr):
    client = User.objects.get(id = request.user.id)

    def generateOrderID():
        return str(random.randint(1000000000, 9999999999) * client.id * random.randint(3, 7))[:10]

    orderID = generateOrderID()

    while Order.objects.filter(order_id = orderID).exists():
        orderID = generateOrderID()

    for cart in Cart.objects.filter(client = client):
        Order.objects.create(order_id = orderID, product = cart.product, client = client)
        cart.delete()

    return redirect('client-orders')

def clientOrders(request):

    queryOrders = '''
    select 
    p.name as productName,
    p.product_id as productCode,
    p.price as productPrice,
    p.album_id as productAlbum,
    count(p.product_id) as productCount,
    o.order_id as orderID,
    o.product_id,
    o.client_id as clientID,
    sum(p.price) as sumForCount,
    p.id
    from Orders as o
    join Products as p
    on p.id = o.product_id
    where clientID = ''' + str(request.user.id) + '''
    group by clientID, productCode, orderID'''
    
    orders_tmp = Order.objects.raw(queryOrders)
    # Нужные поля:
    # productID - код товара
    # productName - имя товара
    # productImage - изображение товара
    # productPrice - цена за единицу товара
    # productCount - количество единиц товара в заказе
    # sumForCount - цена за все единицы указанного товара
    # clientID - id клиента (индекс в таблице)
    # orderID - номер заказа (поле из таблицы Orders, не индекс таблицы)

    class Order_tmp:
        def __init__(self, product, images):
            self.orderID = product.orderID
            self.productID = product.id
            self.productCode = product.productCode
            self.productName = product.productName[:40]
            self.productPrice = product.productPrice
            self.productCount = product.productCount
            self.sumForCount = product.sumForCount
            self.productImages = []
            for img in images:
                self.productImages.append(str(img.img.url))
            self.productImage = self.productImages[0]

    orders = []

    for order in orders_tmp:
        images = Images.objects.filter(album_id = order.productAlbum)
        print('\n-\n', images.query, '\n-\n')
        orders.append(Order_tmp(order, images))

    querySum = '''select
    o.id, o.client_id as clientID, o.order_id as orderID,
    o.date as orderDate,
    sum(p.price) as totalSum,
    s.text as orderStatus, s.colorHEX as statusColor
    from Products as p
    join Orders as o
    on o.product_id = p.id
    join Statuses as s
    on o.status_id = s.id
    where clientID = ''' + str(request.user.id) + '''
    group by orderID, clientID
    order by o.date'''

    sums = Order.objects.raw(querySum)
    # Нужные поля:
    # clientID - id клиента (индекс в таблице)
    # orderID - номер заказа (поле из таблицы Orders, не индекс таблицы)
    # totalSum - сумма за весь заказ
    # orderStatus - статус заказа
    # statusColor - цвет статуса

    # print('\n\n\t\t\t---Заказы клиента: ', orders.query, '\n')
    # print('\n\n\t\t\t---Cуммы заказов клиента: ', sums.query, '\n')

    

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/client-orders.html',
        {
            'orders': orders,
            'sums': sums,
            'orders': orders,
            'title':'Заказы',
            'year':datetime.now().year,
        }
    )

def approveOrder(request, parametr):

    orders = Order.objects.filter(order_id = parametr)
    status = Status.objects.get(text = 'Подтвержден')

    for order in orders:
        order.status = status
        order.save()

    return redirect('manager-orders')

def rejectOrder(request, parametr):
    orders = Order.objects.filter(order_id = parametr)
    status = Status.objects.get(text = 'Отклонен')

    for order in orders:
        order.status = status
        order.save()

    return redirect('manager-orders')

def resetOrder(request, parametr):
    orders = Order.objects.filter(order_id = parametr)
    status = Status.objects.get(text = 'В обработке')

    for order in orders:
        order.status = status
        order.save()

    return redirect('manager-orders')

def deleteOrder(request, parametr):
    orders = Order.objects.filter(order_id = parametr)

    for order in orders:
        order.delete()

    return redirect('manager-orders')

def imgs(request):
    query = 'select * from Images'

    images = Images.objects.raw(query)

    print("\n\n\t\t\t---Картинки:\n\n" + str(images.query) + "\n\n")

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/imgs.html',
        {
            'images': images,
            'year':datetime.now().year,
            }
        )

def editUser(request):
    if request.method == "POST":
        userForm = EditUserForm(request.POST)
        if userForm.is_valid():
            uf = userForm.save(commit=False)
            client = Client.objects.get(username = request.user.username)
            client.first_name = uf.first_name
            client.last_name = uf.last_name
            client.email = uf.email
            client.phone = uf.phone
            client.save()
            user = User.objects.get(username = request.user.username)
            user.first_name = uf.first_name
            user.last_name = uf.last_name
            user.email = uf.email
            user.save()
            return redirect('profile')
    else:
        client = Client.objects.get(username = request.user.username)
        userForm = EditUserForm(initial={
        'first_name': client.first_name,
        'last_name': client.last_name,
        'email': client.email,
        'phone': client.phone,
        }) # создание объекта формы для ввода данных нового пользователя
    return render(
        request,
        'app/edit-user.html',
        {
            'userForm': userForm, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def profile(request):
    client = Client.objects.get(username = request.user.username)
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/profile.html',
        {
            'client' : client,
            'year':datetime.now().year,
        }
    )

def addProduct(request):
    # assert isinstance(request, HttpRequest)
    if request.method == "POST":
        # addAlbumForm = AddAlbumForm(request.POST)
        # if addAlbumForm.is_valid():
        #     a = addAlbumForm.save(commit=False)
        #     if not Album.objects.filter(name = a.name).exist():
        #         Album.objects.create(name = a.name)
        #     album = Album.objects.get(name = a.name)
        
        # addImagesForm = AddImagesForm(request.POST)
        # if addImagesForm.is_valid():
        #     i = addImagesForm.save(commit=False)
        #     for img in i.images:
        #         Images.objects.create(album = album, img = img)


        addProductForm = AddProductForm(request.POST, request.FILES)
        files = request.FILES.getlist('img_collection')
        print(files)
        if addProductForm.is_valid():
            pf = addProductForm.save(commit=False)
            print('\n\n\n HELLOOOOOOO?', files, '\n\n\n')
            if not Album.objects.filter(name = pf.album_name).exists():
                Album.objects.create(name = pf.album_name)
            album = Album.objects.get(name = pf.album_name)

            if not Categories.objects.filter(name = pf.category).exists():
                Categories.objects.create(name = pf.category)
            category = Categories.objects.get(name = pf.category)

            Product.objects.create(
                product_id = pf.product_id,
                name = pf.product_name,
                album = album,
                description_short = pf.description_short,
                description_full = pf.description_full,
                category = category,
                price = pf.price
            )

            for file in files:
                Images.objects.create(album = album, img = file)

            # Images.objects.create(album = album, img = pf.img_collection)
            print(pf.img_collection)
            return redirect('catalog')
    else:
        addAlbumForm = AddAlbumForm()
        addImagesForm = AddImagesForm()
        addProductForm = AddProductForm()
    return render(
        request,
        'app/add-product.html',
        {
            # 'addAlbumForm': addAlbumForm,
            # 'addImagesForm': addImagesForm,
            'addProductForm': addProductForm,
            'title': 'Добавть продукт',
            'year':datetime.now().year,
        }
    )
