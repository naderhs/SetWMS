from django.urls import path
from set_app import views

# TEMPLATE URLS!
app_name = 'set_app'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),

    # Dashboard URL patters
    path('dashboard/', views.dashboard, name='dashboard'),

    # Warehouse URL patterns
    path('warehouses/', views.WarehouseListView.as_view(), name='warehouse_list'),
    path('warehouses/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse_detail'),
    path('warehouse_create/', views.WarehouseCreateView.as_view(), name='warehouse_create'),
    path('warehouse_update/<int:pk>/', views.WarehouseUpdateView.as_view(), name='warehouse_update'),
    path('warehouse_delete/<int:pk>/', views.WarehouseDeleteView.as_view(), name='warehouse_delete'),

    # Customer URL patterns
    path('customers/', views.CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', views.CustomerListView2, name='customer_detail'),
    # path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer_detail'),
    path('customer_create/', views.CustomerCreateView.as_view(), name='customer_create'),
    path('customer_update/<int:pk>/', views.CustomerUpdateView.as_view(), name='customer_update'),
    path('customer_delete/<int:pk>/', views.CustomerDeleteView.as_view(), name='customer_delete'),

    # Product URL patters
    # path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/', views.ProductListView, name='product_list'),
    path('products/active_products/', views.ActiveProductsView, name='active_product_list'),
    path('product_create/', views.ProductCreateView, name='product_create'),
    path('product_update/<int:pk>/', views.ProductUpdateView, name='product_update'),
    path('product_delete/<int:pk>/', views.ProductDeleteView, name='product_delete'),

    # Driver URL pattens
    path('driver_create/', views.DriverCreateView.as_view(), name='driver_create'),

    # Download or view PDF
    path('customer/pdf_view/', views.CustomerViewPDF.as_view(), name="customer_pdf_view"),
    path('customer/pdf_download/', views.CustomerDownloadPDF.as_view(), name="customer_pdf_download"),

]
