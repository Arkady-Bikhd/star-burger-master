from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Place(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=100,
        blank=True,
        unique=True,
    )
    latitude = models.FloatField(
        'Широта',
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        blank=True,
        null=True,
        )
    longitude = models.FloatField(
        'Долгота',
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        blank=True,
        null=True,
        )
    updated_at = models.DateTimeField(
        'Обновлено',
        null=True,        
    )

    def __str__(self):
        return f'{self.address} - {self.updated_at}'
