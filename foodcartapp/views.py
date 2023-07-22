import json

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
        check, errormessage = check_order_products(order_products)
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
    except KeyError:
        errormessage = 'Продуктов нет. products: Обязательное поле.'    
    return Response({
        errormessage,
    })


def check_order_products(order_products):
    errormessage = ''
    check = True
    if order_products == None:
        check = False
        errormessage = 'Продукты — это null. products: Это поле не может быть пустым.'
        return check, errormessage 
    elif not isinstance(order_products, list):
        check = False
        errormessage = 'Продукты — это не список, а строка.products: Ожидался list со значениями, но был получен "str".'
        return check, errormessage
    elif len(order_products) == 0:
        check = False
        errormessage = 'Продукты — пустой список. products: Этот список не может быть пустым.'
        return check, errormessage     
    