from django.shortcuts import redirect
from django.urls import path

from . import views


def favicon_redirect(request):
    return redirect('/static/favicon/favicon.ico')


app_name = 'flair'
urlpatterns = [
    path('', lambda request: redirect('/set', permanent=False)),
    path('wiki', views.wiki, name='wiki'),
    path('set', views.set_flair_url, name='set_flair_url'),
    path('submit', views.submit, name='submit'),
    path('favicon.ico', favicon_redirect),
]
