from django.urls import path

from . import views

app_name = 'archive'
urlpatterns = [
    path('download/', views.download, name='download')
]
