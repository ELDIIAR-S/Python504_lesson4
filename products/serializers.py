from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Product, Review


# ====================================================
# Сериализаторы отображения (GET)
# ====================================================

class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryDetailSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']


class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product_id']


# ====================================================
# Сериализаторы валидации входных данных (POST / PUT)
# ====================================================

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(
        min_length=2,
        max_length=100,
        required=True,
        error_messages={
            'required': 'Поле "name" обязательно для заполнения.',
            'blank': 'Поле "name" не должно быть пустым.'
        }
    )

    def validate_name(self, name):
        category_id = self.context.get('category_id')
        queryset = Category.objects.filter(name__iexact=name)
        if category_id:
            queryset = queryset.exclude(id=category_id)
        if queryset.exists():
            raise ValidationError('Категория с таким названием уже существует.')
        return name


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(
        min_length=3,
        max_length=150,
        required=True,
        error_messages={
            'required': 'Поле "title" обязательно для заполнения.',
            'min_length': 'Название товара должно быть длиной от 3 символов.'
        }
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        default=''
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        required=True,
        error_messages={
            'required': 'Поле "price" обязательно для заполнения.',
            'min_value': 'Цена должна быть строго больше нуля.'
        }
    )
    category_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'Поле "category_id" обязательно для заполнения.'}
    )

    def validate_category_id(self, category_id):
        if not Category.objects.filter(id=category_id).exists():
            raise ValidationError(f'Категория с ID {category_id} не найдена.')
        return category_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(
        min_length=3,
        max_length=1000,
        required=True,
        error_messages={
            'required': 'Поле "text" обязательно для заполнения.',
            'min_length': 'Текст отзыва должен содержать не менее 3 символов.'
        }
    )
    stars = serializers.IntegerField(
        min_value=1,
        max_value=5,
        required=True,
        error_messages={
            'required': 'Поле "stars" обязательно для заполнения.',
            'min_value': 'Оценка не может быть меньше 1.',
            'max_value': 'Оценка не может быть больше 5.'
        }
    )
    product_id = serializers.IntegerField(
        required=True,
        error_messages={'required': 'Поле "product_id" обязательно для заполнения.'}
    )

    def validate_product_id(self, product_id):
        if not Product.objects.filter(id=product_id).exists():
            raise ValidationError(f'Товар с ID {product_id} не найден.')
        return product_id