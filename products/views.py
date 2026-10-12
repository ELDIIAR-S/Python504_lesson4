from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    CategoryDetailSerializer, CategoryValidateSerializer,
    ProductDetailSerializer, ProductValidateSerializer,
    ReviewDetailSerializer, ReviewValidateSerializer
)

# /api/v1/categories/ и /api/v1/categories/<id>/

@api_view(['GET', 'POST'])
def category_list_create_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategoryDetailSerializer(categories, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        validator = CategoryValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(data={'errors': validator.errors}, status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.create(name=validator.validated_data.get('name'))
        return Response(data=CategoryDetailSerializer(category).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Категория не найдена.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategoryDetailSerializer(category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        validator = CategoryValidateSerializer(data=request.data, context={'category_id': id})
        if not validator.is_valid():
            return Response(data={'errors': validator.errors}, status=status.HTTP_400_BAD_REQUEST)

        category.name = validator.validated_data.get('name')
        category.save()
        return Response(data=CategoryDetailSerializer(category).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# /api/v1/products/ и /api/v1/products/<id>/


@api_view(['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        serializer = ProductDetailSerializer(products, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        validator = ProductValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(data={'errors': validator.errors}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.create(
            title=validator.validated_data.get('title'),
            description=validator.validated_data.get('description', ''),
            price=validator.validated_data.get('price'),
            category_id=validator.validated_data.get('category_id')
        )
        return Response(data=ProductDetailSerializer(product).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.select_related('category').get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Товар не найден.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductDetailSerializer(product)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        validator = ProductValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(data={'errors': validator.errors}, status=status.HTTP_400_BAD_REQUEST)
        product.title = validator.validated_data.get('title')
        product.description = validator.validated_data.get('description', '')
        product.price = validator.validated_data.get('price')
        product.category_id = validator.validated_data.get('category_id')
        product.save()
        return Response(data=ProductDetailSerializer(product).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# /api/v1/reviews/ и /api/v1/reviews/<id>/

@api_view(['GET', 'POST'])
def review_list_create_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewDetailSerializer(reviews, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        validator = ReviewValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(data={'errors': validator.errors}, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(
            text=validator.validated_data.get('text'),
            stars=validator.validated_data.get('stars'),
            product_id=validator.validated_data.get('product_id')
        )
        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Отзыв не найден.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewDetailSerializer(review)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        validator = ReviewValidateSerializer(data=request.data)
        if not validator.is_valid():
            return Response(data={'errors': validator.errors}, status=status.HTTP_400_BAD_REQUEST)

        review.text = validator.validated_data.get('text')
        review.stars = validator.validated_data.get('stars')
        review.product_id = validator.validated_data.get('product_id')
        review.save()
        return Response(data=ReviewDetailSerializer(review).data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)