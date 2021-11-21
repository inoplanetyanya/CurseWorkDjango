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

class Сategories(models.Model):
  name = models.CharField(max_length = 150, default = 'Прочее', unique = True, verbose_name = 'Название категории')

  def __str__(self):
    return str(self.id) + " | " + self.name

  class Meta:
    db_table = "Сategories"
    verbose_name = "Категория"
    verbose_name_plural = "Категории"

class Product(models.Model):
  product_id = models.CharField(max_length = 150, unique = True, verbose_name = 'Код товара')
  name = models.CharField(max_length = 150, verbose_name = 'Название товара')
  price = models.DecimalField(max_digits=10, decimal_places = 2, verbose_name = 'Цена товара', default = 9999999)
  image = models.FileField(default = 'placeholder/placeholder.png', verbose_name = 'Путь к картинке')
  description = models.TextField(verbose_name = 'Описание')
  category = models.ForeignKey(Сategories, on_delete = models.CASCADE, verbose_name = 'Категория')

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
  product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Товар')

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
    return '%s | %s' % (self.id, self.text)

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

admin.site.register(Product)
admin.site.register(Сategories)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Status)


