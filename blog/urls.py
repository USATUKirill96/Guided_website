from django.urls import path
from . import views

app_name = 'blog'

"""Маршрут для каждого поста составляется по шаблону год/месяц/день/слаг. В один день может существовать только 
один пост с одинаковым слагом. Слаг формируется из названия, но его можно сменить вручную"""

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
]