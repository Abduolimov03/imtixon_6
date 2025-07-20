from . import views
from django.urls import path
from .views import (
    ProductDetail,
    ProductDelete,
    ProductUpdate,
    ProductCreate
)

urlpatterns = [
    path('product/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('product/create/', ProductCreate.as_view(), name='product-create'),
    path('product/update/<int:pk>/', ProductUpdate.as_view(), name='product-update'),
    path('product/delete/<int:pk>/', ProductDelete.as_view(), name='product-delete'),
    path('', views.category_list, name='product_list'),
    path('category/<int:category_id>/', views.product_by_category, name='product_by_category'),
    path('add-comment/<int:pk>/', views.add_comment, name='add_comment'),

]


