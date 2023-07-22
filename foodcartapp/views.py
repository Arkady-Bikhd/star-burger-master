import json
import phonenumbers

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, OrderItem, Product


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    errormessage = ''
    order_description = request.data
    try:
        order_products = order_description['products']
        firstname = order_description['firstname']
        lastname = order_description['lastname']
        phone_number = order_description['phonenumber']
        address = order_description['address']
        check, errormessage = check_order_fields(
            order_products,
            [
                firstname,
                lastname,
                phone_number,
                address,
            ]
        )
        print(check)
        print(errormessage)
        if check:
            order = Order.objects.create(
                firstname=firstname,
                lastname=lastname,
                phone_number=phone_number,
                address=address
            )
            for order_product in order_products:
                product_id = order_product['product']
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_amount=order_product['quantity']
                )
    except KeyError as missing_key:
        errormessage = f'Не введены данные. {missing_key}: Обязательное поле.'
    return Response({
        errormessage,
    })


def check_order_products(order_products):
    errormessage = ''
    check = True
    max_product_id = Product.objects.count()
    if order_products == None:
        check = False
        errormessage = 'products: Это поле не может быть пустым.'
        return check, errormessage
    elif not isinstance(order_products, list):
        check = False
        errormessage = 'products: Ожидался list со значениями, но был получен "str".'
        return check, errormessage
    elif len(order_products) == 0:
        check = False
        errormessage = 'products: Этот список не может быть пустым.'
        return check, errormessage
    for order_product in order_products:
        product_id = order_product['product']
        if not product_id:
            check = False
            errormessage = 'product: Это поле не может быть пустым.'
            return check, errormessage
        elif product_id > max_product_id:
            check = False
            errormessage = f'product: Недопустимый первичный ключ {product_id}.'
            return check, errormessage
    return check, errormessage


def check_order_fields(order_products, fields: list):
    print('check_order_fields')
    product_check, product_errormessage = check_order_products(order_products)
    fields_check = True
    fields_errormessage = str()
    for field_number, field in enumerate(fields):
        field_name = 'firstname'
        if field_number == 1:
            field_name = 'lastname'
        if field_number == 2:
            field_name = 'phonenumber'
        if field_number == 3:
            field_name = 'address'
        check, errormessage = check_field(field, field_number)
        if not check:
            fields_errormessage += f'{field_name}:{errormessage} '
            fields_check = False
    return product_check and fields_check, f'{product_errormessage} {fields_errormessage}'


def check_field(field, field_number):
    print('check_field')
    errormessage = ''
    check = True
    if field == None:
        check = False
        errormessage = 'не может быть пустым'
        return check, errormessage
    elif field == '':
        check = False
        errormessage = 'не может быть пустым'
        return check, errormessage
    elif isinstance(field, list):
        check = False
        errormessage = 'не может быть списком'
        return check, errormessage
    elif field_number == 2:
        check, errormessage = check_phone_number(field)
        return check, errormessage
    else:
        return check, errormessage


def check_phone_number(field):
    check = True
    errormessage = ''
    try:
        phone_number = phonenumbers.parse(field, 'RU')
        if not phonenumbers.is_valid_number(phone_number):
            check = False
            errormessage = 'неправильный номер телефона'
        return check, errormessage
    except phonenumbers.NumberParseException:
        check = False
        errormessage = 'неправильный номер телефона'
        return check, errormessage
