from django.core.validators import MinValueValidator
from django.db import models


class Item(models.Model):

    name = models.CharField(
        verbose_name='Наименование товара',
        max_length=30,
        unique=True
    )
    description = models.TextField(
        verbose_name='Описание товара',
        help_text='Введите ставку в процентах',
    )
    price = models.DecimalField(
        verbose_name='Стоимость товара',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0)]
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name