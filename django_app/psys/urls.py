from . import views
from django.urls import path

urlpatterns = [
    path('',views.index,name='index'),
    path('', views.header, name='header'),
    path('MainMenu/', views.mainmenu, name='MainMenu'),
    path('CustomerManagementMenu/', views.customermanagementmenu, name='CustomerManagementMenu'),

]
