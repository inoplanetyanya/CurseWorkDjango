"""
Definition of models.
"""

from django.core.files import storage
from django.db import models

# Create your models here.
from datetime import datetime
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.fields import CharField

class ProductInfo(models.Model):
  album_name = models.CharField(max_length=150)
  img_collection = models.FileField(verbose_name='asdf')
  product_id = models.IntegerField()
  product_name = models.CharField(max_length=150)
  description_short = models.TextField(max_length=1000)
  description_full = models.TextField(max_length=999999)
  category = models.CharField(max_length=150)
  price = models.DecimalField(decimal_places = 2, max_digits=12)

class Client(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  username = models.CharField(max_length=150, unique=True)
  first_name = models.CharField(max_length=150)
  last_name = models.CharField(max_length=150)
  email = models.EmailField(max_length=150)
  phone = models.CharField(max_length=150)

  class Meta:
    db_table = "Clients"
    verbose_name = "Клиент"
    verbose_name_plural = "Клиенты"

class Categories(models.Model):
  name = models.CharField(max_length = 150, default = 'Прочее', unique = True, verbose_name = 'Название категории')

  def __str__(self):
    return self.name

  class Meta:
    db_table = "Categories"
    verbose_name = "Категория"
    verbose_name_plural = "Категории"

class Album(models.Model):
  name = models.CharField(max_length = 150, unique = True, verbose_name = 'Название альбома')

  def __str__(self):
    return self.name

  class Meta:
    db_table = "Albums"
    verbose_name = "Альбом"
    verbose_name_plural = "Альбомы"

class Images(models.Model):
  album = models.ForeignKey(Album, on_delete = models.CASCADE, verbose_name = 'Альбом')
  img = models.FileField(default = 'placeholder/placeholder.png', verbose_name = 'Путь к картинке')

  def __str__(self):
    return self.album.name + " | - " + self.img.url

  class Meta:
    db_table = "Images"
    verbose_name = "Картинка"
    verbose_name_plural = "Картинки"

class News(models.Model):
  title = models.CharField(max_length=150, verbose_name='Заголовок новости')
  text = models.TextField(verbose_name='Текст новости')
  image = models.FileField(default = 'placeholder/placeholder.png', verbose_name = 'Изображение к новости')
  date = models.DateField(default=datetime.now(), verbose_name='Дата публикации')

  def __str__(self) -> str:
    return self.title

  class Meta:
    db_table = "News"
    ordering = ["-date"]
    verbose_name = "Новость"
    verbose_name_plural = "Новости"

class Product(models.Model):
  product_id = models.CharField(max_length = 150, unique = True, verbose_name = 'Код продукта')
  name = models.CharField(max_length = 150, verbose_name = 'Название продукта')
  price = models.DecimalField(max_digits=10, decimal_places = 2, verbose_name = 'Цена продукта', default = 9999999)
  album = models.ForeignKey(Album, on_delete = models.CASCADE, verbose_name = 'Альбом')
  description_short = models.CharField(max_length=1000, verbose_name='Краткое описание')
  description_full = models.TextField(verbose_name = 'Полное описание')
  category = models.ForeignKey(Categories, on_delete = models.CASCADE, verbose_name = 'Категория')

  def get_absolute_url(self):
    return reverse("product", args=[str(self.id)])

  def __str__(self):
    return self.product_id + " | " + self.name

  class Meta:
    db_table = "Products"
    ordering = ["product_id"]
    verbose_name = "Продукт"
    verbose_name_plural = "Продукты"

class Comment(models.Model):
  text = models.TextField(verbose_name = 'Отзыв')
  date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
  author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
  product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Продукт')

  def __str__(self):
    return '%s %s' % (self.date, self.author)

  class Meta:
    db_table = "Comments"
    ordering = ["-date"]
    verbose_name = "Отзыв"
    verbose_name_plural = "Отзывы"

class Status(models.Model):
  text = models.CharField(max_length = 150, unique = True, verbose_name = 'Наименование сатуса')
  colorHEX = models.CharField(max_length = 6, verbose_name = 'Цвет статуса HEX')

  def __str__(self):
    return self.text

  class Meta:
    db_table = "Statuses"
    ordering = ["id"]
    verbose_name = "Статус"
    verbose_name_plural = "Статусы заказов"

class Order(models.Model):
  order_id = models.IntegerField(null = False, verbose_name = 'Номер заказа')
  product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = "Продукт")
  client = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Клиент")
  status = models.ForeignKey(Status, default = 1, on_delete = models.CASCADE, verbose_name = "Статус")
  date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")

  def __str__(self):
    return str(self.id) + " | - " + self.product.product_id + " - | " + str(self.date)

  def get_absolute_url(self):
    return reverse("client-orders", args=[str(self.id)])

  class Meta:
    db_table = "Orders"
    ordering = ["date"]
    verbose_name = "Заказ"
    verbose_name_plural = "Заказы"

class Cart(models.Model):
  product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = "Продукт")
  client = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Клиент")

  def __str__(self):
    return self.client.username + " | - " + self.product.product_id

  class Meta:
    db_table = "Carts"
    verbose_name = "Корзина"
    verbose_name_plural = "Корзины"

# admin.site.register(Product)
# admin.site.register(Categories)
# admin.site.register(Comment)
# admin.site.register(Order)
# admin.site.register(Cart)
# admin.site.register(Status)
# admin.site.register(Images)
# admin.site.register(Album)
# admin.site.register(News)