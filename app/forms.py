"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import fields
from django.utils.translation import ugettext_lazy as _

from .models import Client, Comment, Images, Product, Album, ProductInfo

class BootstrapAuthenticationForm(AuthenticationForm):
  """Authentication form which uses boostrap CSS."""
  username = forms.CharField(max_length=254,
  widget=forms.TextInput({
    'class': 'form-control login-input',
    'placeholder': 'Имя пользователя'}))
  password = forms.CharField(label=_("Password"),
    widget=forms.PasswordInput({
      'class': 'form-control login-input',
      'placeholder':'Пароль'}))

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ('text',)

class EditUserForm(forms.ModelForm):
  first_name = forms.CharField(max_length=150)
  last_name = forms.CharField(max_length=150)
  email = forms.CharField(max_length=150)
  phone = forms.CharField(max_length=150)
  class Meta:
    model = Client
    fields = ['first_name', 'last_name', 'email', 'phone']

class AddAlbumForm(forms.ModelForm):
  name = forms.CharField(required=True, max_length=150)
  class Meta:
    model = Album
    fields = ['name']

class AddImagesForm(forms.ModelForm):
  album = forms.CharField(required=True, max_length=150)
  images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
  class Meta:
    model = Images
    fields = ['album']

class AddProductForm(forms.ModelForm):
  # product_id = forms.CharField(required=True, max_length = 150)
  # product_name = forms.CharField(required=True, max_length = 150)
  # price = forms.DecimalField(required=True, max_digits=10)
  # album_name = forms.CharField(required=True, max_length = 150)
  # description_short = forms.Textarea()
  # description_full = forms.Textarea()
  # category = forms.CharField(required=True, max_length=150)
  # images = forms.CharField(required=True, max_length=150)
  img_collection = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

  class Meta:
    model = ProductInfo
    fields = ['product_id', 'product_name', 'price', 'album_name', 'description_full', 'description_short', 'category']