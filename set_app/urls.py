from django.urls import path, include
from set_app import views

# TEMPLATE URLS!
app_name = 'set_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('warehouses/', views.WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('warehouse_create/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouse_update/<int:pk>/', views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouse_delete/<int:pk>/', views.WarehouseDeleteView.as_view(), name='warehouse_delete'),

]
