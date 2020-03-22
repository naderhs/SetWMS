from django.urls import path, include
from set_app import views

# TEMPLATE URLS!
app_name = 'set_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('warehouse_page/', views.warehouse_view, name='warehouse_page'),
]
