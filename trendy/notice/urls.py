from django.urls import path
from . import views

app_name = 'notice'
urlpatterns = [
    path('', views.main, name = 'main'),
    path('board/', views.BoardListView.as_view(), name = 'board'),
    path('board=<int:pk>/', views.boadet, name = 'boadet'),
    path('board=<int:pk>/delete', views.boadel, name = 'boadel'),
    path('notice/', views.NoticeListView.as_view(), name='notice'),
    path('notice=<int:pk>/', views.notdet, name = 'notdet'),
    path('write/', views.write, name = 'write'),    
]