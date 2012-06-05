#coding:utf8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from dish.models import Food, Restaurant, Order
from django.utils import simplejson
from django.core import serializers
from dish.utils.decorators import login_required as user_login_required
from django.contrib.auth.decorators import login_required as admin_login_required

import logging
logger = logging.getLogger('test')

@csrf_exempt
def order_cancle(request):
    user = request.user
    account = request.account

    #if user.is_authenticated() == False:
    #    if account.is_authenticated() == False:
    #        return HttpResponse('Fail')

    order_id = request.POST.get('order_id', False)
    if order_id:
        try:
            order = Order.objects.get(pk=order_id)
        except:
            raise
        if order.status == 'b' and (  #Book
            user.is_authenticated() or order.username==account):
            order.status = 'a' #cAncel
            order.save()
            return HttpResponse('Success')

    return HttpResponse('Fail')

@csrf_exempt
def order_finish(request):
    return HttpResponse()

@csrf_exempt
@user_login_required
def food_list(request):
    r_id = request.GET.get('restaurant', False)
    try:
        restautant_id = r_id.split('_')[1]
        restautant = Restaurant.objects.get(pk=restautant_id)
    except Restaurant.DoesNotExist:
        return HttpResponse()
    _food = Food.objects.filter(restaurant=restautant).exclude(exist=False)
    #food_list = [] 
    #for dish in dishes:
    #    food_list.append("%s$%s$%s"%(dish.pk, dish.dish_name, dish.price))
    ##result = simplejson.dumps(food_list)
    data = serializers.serialize("json", _food, ensure_ascii=False)
    return HttpResponse(data)

@csrf_exempt
@user_login_required
def order_book_confirm(request):
    _p = request.POST
    account = request.account
    if _p and account.is_authenticated():
        try:
            _food_id = _p.get('food_id', False)
            date = _p.get('date', False)
            dish_character = _p.get('dish_character', False)
            remark = _p.get('remark', '')
        except:
            return HttpResponse()
        food_id = _food_id[2:]
        order = Order.objects.create_order(account, food_id, date, dish_character, remark)
        if order:
            context = {
                'order_id':order.pk,
                'character':order.character,
                'food_name':order.food.name,
                'food_price':order.food.price,
                'restaurant':order.restaurant.name,
                'order_date':order.date,
                'remark':order.remark,
                'dish_character':order.dish_character(),
            }
            data = simplejson.dumps(context)
            return HttpResponse(data)
    return HttpResponse("Fail")

@csrf_exempt
@admin_login_required
def confirm_order(request):
    _orders = request.POST.get("confirm_orders", False)
    order_id_list = _orders.split(',')
    result = Order.objects.confirm_orders(order_id_list)
    return HttpResponse(result)

@csrf_exempt
@admin_login_required
def finish_order(request):
    _orders = request.POST.get("finish_orders", False)
    order_id_list = _orders.split(',')
    result = Order.objects.finish_orders(order_id_list)
    return HttpResponse(result)

@csrf_exempt
@user_login_required
def new_food(request):
    _p = request.POST
    restaurant_id = _p.get('restaurant', False)
    food_name = _p.get('food_name', False)
    food_price = _p.get('food_price', False)
    if restaurant_id and food_name and food_price and food_price.isdigit():
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            return HttpResponse('Fail')
        try:
            food_name = food_name.split()[0]
            p_food_name = ''.join([str(request.account.pk), ":" , food_name])
            food = Food(restaurant=restaurant, name=p_food_name, price=food_price)
            food.save()
        except:
            return HttpResponse('Fail')
        return HttpResponse(','.join([str(food.pk), food.name, food.price]))
    return HttpResponse('Fail')

