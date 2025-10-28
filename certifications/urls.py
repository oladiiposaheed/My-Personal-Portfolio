from django.urls import path
from . import views

app_name = 'certifications'

urlpatterns = [
    path('', views.certification_list, name='certification_list'),
    path('<slug:slug>/', views.certification_detail, name='certification_detail'),
]