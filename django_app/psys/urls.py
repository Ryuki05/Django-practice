from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'psys'

urlpatterns = [
    # メインメニュー
    path('', views.MainMenuView.as_view(), name='main_menu'),

    # ログイン関連
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='psys:main_menu'), name='logout'),

     path('signup/', views.SignUpView.as_view(), name='signup'),

    # 得意先管理
    path('customer/', views.CustomerListView.as_view(), name='customer_list'),
    path('customer/add/', views.CustomerCreateView.as_view(), name='customer_add'),
    path('customer/<str:customer_code>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer/<str:customer_code>/edit/', views.CustomerUpdateView.as_view(), name='customer_edit'),
    path('customer/<str:customer_code>/delete/', views.CustomerDeleteView.as_view(), name='customer_delete'),

    # 受注管理
    path('order/', views.OrderListView.as_view(), name='order_list'),
    path('order/add/', views.OrderCreateView.as_view(), name='order_add'),
    path('order/<str:order_number>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('order/<str:order_number>/edit/', views.OrderUpdateView.as_view(), name='order_edit'),
    path('order/<str:order_number>/delete/', views.OrderDeleteView.as_view(), name='order_delete'),

    # 商品管理
    path('item/', views.ItemListView.as_view(), name='item_list'),
    path('item/add/', views.ItemCreateView.as_view(), name='item_add'),
    path('item/<str:item_code>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('item/<str:item_code>/edit/', views.ItemUpdateView.as_view(), name='item_edit'),
    path('item/<str:item_code>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),

    path('employee/create/', views.employee_create, name='employee_create'),
] 

