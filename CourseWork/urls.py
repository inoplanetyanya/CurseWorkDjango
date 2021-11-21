"""
Definition of urls for CourseWork.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
from django.views.generic.base import RedirectView

import app.forms
import app.views

from django.conf.urls import include
from django.contrib import admin

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^catalog$', app.views.catalog, name='catalog'),
    url(r'^(?P<parametr>\d+)/$', app.views.product, name='product'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^news$', app.views.news, name='news'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^client-cart$', app.views.clientCart, name='client-cart'),
    url(r'^client-orders$', app.views.clientOrders, name='client-orders'),
    url(r'^manager-orders$', app.views.managerOrders, name='manager-orders'),
    url(r'^registration$', app.views.registration, name='registration'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Вход',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()