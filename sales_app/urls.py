from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.sales_login, name='sales_login'),
    path('sales_logout', views.sales_logout, name='sales_logout'),

    path('index', views.index, name='index'),
    path('manage_category', views.manage_category, name='manage_category'),
    path('edit_category<int:category_id>/', views.edit_category, name='edit_category'),
    path('edit_category<int:category_id>/', views.delete_category, name='delete_category'),
    path('manage_units', views.manage_units, name='manage_units'),
    path('edit_unit<int:unit_id>/', views.edit_unit, name='edit_unit'),
    path('delete_unit<int:unit_id>/', views.delete_unit, name='delete_unit'),
    path("manage_products", views.manage_products, name="manage_products"),
    path("add_material", views.add_material, name="add_material"),
    path("edit_material/<int:pk>/", views.edit_material, name="edit_material"),
    path("delete_material/<int:pk>/", views.delete_material, name="delete_material"),

    path('salesman/', views.manage_salesman, name='manage_salesman'),
    path('add_salesman/', views.add_salesman, name='add_salesman'),  # Ensure trailing slash
    path('edit_salesman/<int:salesman_id>/', views.edit_salesman, name='edit_salesman'),
    path('delete_salesman/<int:salesman_id>/', views.delete_salesman, name='delete_salesman'),

    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('manage_invoices', views.manage_invoices, name='manage_invoices'),

    path('invoice', views.invoice, name='invoice'),
    path('update-cart-item/', views.update_cart_item, name='update_cart_item'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('save-invoice/', views.save_invoice, name='save_invoice'),

    path('search-products/', views.search_products, name='search_products'),
    path('search-salesmen/', views.search_salesmen, name='search_salesmen'),

    path("invoice_details/<int:invoice_id>/", views.invoice_details, name="invoice_details"),
    path("edit_invoice/<int:invoice_id>/", views.edit_invoice, name="edit_invoice"),

    path("add_product_to_invoice/<int:invoice_id>/", views.add_product_to_invoice, name="add_product_to_invoice"),
    path("remove_product/<int:product_id>/", views.remove_product, name="remove_product"),
    path('delete-invoice/<int:invoice_id>/', views.delete_invoice, name='delete_invoice'),
    path('get_sales_data/', views.get_sales_data, name='get_sales_data'),



]