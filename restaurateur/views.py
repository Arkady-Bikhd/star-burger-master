import requests

from datetime import date
from django import forms
from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.db.models import Q
from django.conf import settings # YANDEX_API_KEY

from geopy import distance

from foodcartapp.models import Product, Restaurant, Order, OrderItem, RestaurantMenuItem
from distances.models import Place


class Login(forms.Form):
    username = forms.CharField(
        label='Логин', max_length=75, required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Укажите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль', max_length=75, required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )


class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = Login()
        return render(request, "login.html", context={
            'form': form
        })

    def post(self, request):
        form = Login(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if user.is_staff:  # FIXME replace with specific permission
                    return redirect("restaurateur:RestaurantView")
                return redirect("start_page")

        return render(request, "login.html", context={
            'form': form,
            'ivalid': True,
        })


class LogoutView(auth_views.LogoutView):
    next_page = reverse_lazy('restaurateur:login')


def is_manager(user):
    return user.is_staff  # FIXME replace with specific permission


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_products(request):
    restaurants = list(Restaurant.objects.order_by('name'))
    products = list(Product.objects.prefetch_related('menu_items'))

    products_with_restaurant_availability = []
    for product in products:
        availability = {item.restaurant_id: item.availability for item in product.menu_items.all()}
        ordered_availability = [availability.get(restaurant.id, False) for restaurant in restaurants]

        products_with_restaurant_availability.append(
            (product, ordered_availability)
        )

    return render(request, template_name="products_list.html", context={
        'products_with_restaurant_availability': products_with_restaurant_availability,
        'restaurants': restaurants,
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_restaurants(request):
    return render(request, template_name="restaurants_list.html", context={
        'restaurants': Restaurant.objects.all(),
    })


@user_passes_test(is_manager, login_url='restaurateur:login')
def view_orders(request):
    order_items = list()
    orders = list(Order.objects.filter(status='Н'))
    for order in orders:
        order_item = fill_order_items(order,  order.status)
        order_items.append(order_item)
    orders = list(Order.objects.filter(status='Г'))
    for order in orders:
        order_item = fill_order_items(order,  order.status)
        order_items.append(order_item)       
    return render(request, template_name='order_items.html', context={
        'order_items': order_items,        
    })


def get_availabile_restaurants(order):
    order_items = order.order_items.all()
    restaurant_menu = RestaurantMenuItem.objects.prefetch_related('restaurant')
    restaurants_for_product = list()
    for order_item in order_items:        
        restaurants = [restaurant.restaurant for restaurant in restaurant_menu.filter(product=order_item.product)]
        restaurants_for_product.append(restaurants)
    availabile_restaurants = set(restaurants_for_product[0])
    for restuarant in restaurants_for_product:
        availabile_restaurants = availabile_restaurants.intersection(restuarant)    
    availabile_restaurants = calculate_distance(list(availabile_restaurants), order.address)
    return availabile_restaurants


def fetch_coordinates(apikey, address):    
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def calculate_distance(availabile_restaurants, address):
    availabile_restaurants_coords = list()
    for restaurant in availabile_restaurants:
        restaurant_address_coords = get_place_coords(restaurant.address)
        order_address_coords = get_place_coords(address)
        if restaurant_address_coords and order_address_coords:
            coord_distance = list(
                (restaurant.name, round(distance.distance(
                restaurant_address_coords,
                order_address_coords).km, 2))
            )            
        else:
            coord_distance = list(
                (restaurant.name, 0)
            )            
        availabile_restaurants_coords.append(coord_distance)
    availabile_restaurants_coords.sort(key=lambda restaurant: restaurant[1])
    availabile_restaurants = [{ 'name': restaurant[0],  'distance': restaurant[1]} for restaurant in availabile_restaurants_coords]    
    return availabile_restaurants


def fill_order_items(order, order_status):
    order_value = OrderItem.objects.filter(order=order.id).calculate_order_value()
    availabile_restaurants = None
    if order_status=='Н':        
        availabile_restaurants = get_availabile_restaurants(order)    
    order_item = {
            'id': order.id,
            'firstname': order.firstname,
            'status': order.get_status_display(),
            'payment_method': order.get_payment_method_display(),
            'lastname': order.lastname,
            'phonenumber': order.phonenumber,
            'address': order.address,
            'order_value': order_value,
            'comment': order.comment,
            'restaurant': order.restaurant,
            'availabile_restaurants': availabile_restaurants,
        }
    return order_item


def get_place_coords(address):
    place, created = Place.objects.get_or_create(address=address)    
    if not created:
        return place.latitude, place.longitude
    place_coords = fetch_coordinates(settings.YANDEX_API_KEY, address)    
    if not place_coords:
        Place.objects.filter(address=address).delete()
        return False
    place.latitude, place.longitude = place_coords
    place.updated_at = date.today()
    place.save()
    return place.latitude, place.longitude
