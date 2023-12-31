from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import F
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    ORDER_STATUS = (
        ('З', 'Завершённый'),
        ('Н','Необработанный'),
        ('Г', 'Готовится')
    )
    PAYMENT_METHOD = (
        ('Э', 'Электронно'),
        ('Н', 'Наличностью'),
    )
    firstname = models.CharField(
        'Имя',
        max_length=30,
    )
    lastname = models.CharField(
        'Фамилия',
        max_length=50,
        db_index=True,
    )
    phonenumber = PhoneNumberField(
        'Телефон',
        region='RU',
        db_index=True,
    )
    address = models.CharField(
        'Адрес доставки',
        max_length=100,
    )
    status = models.CharField(
        'Статус',
        max_length=2,
        db_index=True,
        choices=ORDER_STATUS,
        default='Н',
    )
    comment = models.TextField(
        'Комментарий',
        blank=True,
    )
    registered_at = models.DateTimeField(
        'Зарегистрирован:',
        default=timezone.now,
        db_index=True,
        null=True,
        blank=True,
    )
    called_at = models.DateTimeField(
        'Сделан звонок:',
        blank=True,
        db_index=True,
        null=True,
    )
    delivered_at = models.DateTimeField(
        'Доставлено:',
        blank=True,
        db_index=True,
        null=True,
    )
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=2,
        db_index=True,
        choices=PAYMENT_METHOD,
        null=True,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='restaurant',
        verbose_name='Ресторан',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.lastname} {self.firstname}, {self.address}'


class OrderQuerySet(models.QuerySet):
    def calculate_order_value(self):        
        products_value = self.annotate(
            product_value=F('price') * F('quantity')
        )
        order_value = 0
        for product_value in products_value:
            order_value += product_value.product_value
        return order_value


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name='Заказ',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_products',
        verbose_name='Продукт',
    )    
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Количество',
    )
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    objects = OrderQuerySet.as_manager()
