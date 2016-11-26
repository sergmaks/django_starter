"""
    Настройка URLов
"""

from django.conf.urls import url

from . import views

app_name = 'polls'  # пространтсво именя для приложения polls

urlpatterns = [
    # r'^$'                      - регулярное выражение для поиска в URL
    # views.IndexView.as_view()  - функция представления
    # name='index'               - имя URL
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]