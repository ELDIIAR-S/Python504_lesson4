from django.urls import path
from . import views

urlpatterns = [
    # Категории
    path('api/v1/categories/', views.category_list_create_api_view, name='category-list-create'),
    path('api/v1/categories/<int:id>/', views.category_detail_api_view, name='category-detail'),

    # Товары
    path('api/v1/products/', views.product_list_create_api_view, name='product-list-create'),
    path('api/v1/products/<int:id>/', views.product_detail_api_view, name='product-detail'),

    # Отзывы
    path('api/v1/reviews/', views.review_list_create_api_view, name='review-list-create'),
    path('api/v1/reviews/<int:id>/', views.review_detail_api_view, name='review-detail'),
]