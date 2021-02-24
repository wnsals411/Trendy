from django.urls import path
from . import views

app_name = 'notice'
urlpatterns = [
    path('', views.main, name = 'main'),
    path('qna/', views.QnaListView.as_view(), name = 'qna'),
    path('qna=notice/', views.qnanotice, name = 'qnanotice'),
    path('qna=<int:pk>/', views.qnadet, name = 'qnadet'),
    path('qna=<int:pk>/delete', views.qnadel, name = 'qnadel'),
    path('notice/', views.NoticeListView.as_view(), name='notice'),
    path('notice=<int:pk>/', views.notdet, name = 'notdet'),
    path('write/', views.write, name = 'write'),    
]