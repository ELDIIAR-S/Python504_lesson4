from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def str(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(blank=True, default="", verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def str(self):
        return self.title


class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    stars = models.PositiveSmallIntegerField(default=1, verbose_name="Оценка")
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Товар"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def str(self):
        return f"{self.product.title} ({self.stars}★)"