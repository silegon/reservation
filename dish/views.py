#coding:utf8
import datetime
from django.shortcuts import render_to_response
from dish.utils.auth import platform_login, platform_logout
from dish.forms import AuthenticationForm
from django.contrib.auth.forms import AuthenticationForm as AdminAuthenticationForm
from django.contrib.auth import login as platform_admin_login
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import  csrf_protect
from django.template import RequestContext
from dish.models import Account, Restaurant, Order, PayRecord
from dish.utils.decorators import login_required as dish_login_required
from django.contrib.auth.decorators import login_required as admin_login_required

import logging

logger = logging.getLogger('test')

@csrf_protect
def login(request, template_name='dish/login.html',
          authentication_form=AuthenticationForm,
          extra_context=None):

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            platform_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            context = {
                'request':request,
            }
            redirect = request.GET.get('redirect', '/')
            return HttpResponseRedirect(redirect)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()
    context = {
        'form': form,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


@csrf_protect
def register(request, template_name='dish/register.html'):
    context = {}
    if request.method == "POST":
        username = request.POST.get('login_name', False)
        password = request.POST.get('login_password', False)
        real_name = request.POST.get('real_name', False)
        if username and password and real_name:
            account = Account.objects.create_user(username, real_name, password)
            if account:
                return HttpResponse("Success<a href='/login'>login</a>")
        return HttpResponse("Fail")
    else:
        return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


def logout(request):
    platform_logout(request)
    return HttpResponse('成功退出,接下来您可以<a href="/login">登录</a> 或者 <a href="/register">注册</a>') 

@admin_login_required(login_url='/admin_login')
@csrf_protect
def process_order(request, template_name='dish/process_order.html'):
    settlement = PayRecord.objects.finish_pay() #finish payment of bill

    date = request.POST.get('Wdate', False)
    dish_character = request.POST.get('dish_character', False)
    
    if not date or not dish_character: 
        now = datetime.datetime.now()
        date = '-'.join([str(now.year), str(now.month), str(now.day)])
        dish_character = 'l' if now.hour < 13 else 'd'
    booked_order = Order.objects.get_process_order(date, dish_character, status='b') or {}
    confirmed_order = Order.objects.get_process_order(date, dish_character, status='c') or {}
    finished_order = Order.objects.get_process_order(date, dish_character, status='f') or {}

    live_order = [] 
    for dict in (booked_order, confirmed_order, finished_order):
        live_order.extend(dict)
    need_service_account = Account.objects.need_service(dish_character)

    if live_order:
        live_account = map(lambda x:x['username'], live_order)
    else:
        live_account = ''

    not_book = set(need_service_account) - set(live_account)
    extra_book = set(live_account) - set(need_service_account)

    context = {
        'booked_order':booked_order,
        'confirmed_order':confirmed_order,
        'finished_order':finished_order,
        'date':date,
        'dish_character':dish_character,
        'not_book':not_book,
        'extra_book':extra_book,
        'settlement':settlement,
        }
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))

@csrf_protect
@dish_login_required
def records(request, template_name='dish/records.html'):
    account = request.account
    date = request.POST.get('date', False)
    if date:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        date = datetime.datetime.today()
    bmonth = date - datetime.timedelta(30)
    order_finished = Order.objects.filter(date__gte=bmonth, date__lte=date, username=account).order_by('-date')
    pay_list = PayRecord.objects.filter(date__gte=bmonth, date__lte=date, account=account).order_by('-date')
        
    context = {
        'account':account,
        'date':date,
        'order_finished':order_finished,
        'pay_list':pay_list,
    }

    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))


@admin_login_required(login_url='/admin_admin')
def avatar(request):
    value = request.GET.get('not_book_name', False)
    if value:
        try:
            account = Account.objects.get(real_name=value)
        except:
            return HttpResponse("未找到该用户")
        platform_login(request, account)
        return HttpResponseRedirect(reverse('menu'))

    return HttpResponse()

@csrf_protect
@dish_login_required
def menu(request, template_name='dish/menu.html'):
    account = request.account
    context = {
        'account':request.account,
        'date':datetime.date.today(),
        'dish_character':'l' if datetime.datetime.now().hour<13 else 'd',
        'order_booked':Order.objects.order_booked(account),
        'order_confirmed':Order.objects.order_confirmed(account),
        'restaurantes':Restaurant.objects.filter(exist=True),
    }
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))

@csrf_protect
def admin_login(request, template_name='dish/admin_login.html',
               authentication_form=AdminAuthenticationForm,
               extra_context=None):
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            platform_admin_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            context = {
                'request':request,
            }
            redirect = request.GET.get('redirect', 'process_order')
            return HttpResponseRedirect(redirect)
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()
    context = {
        'form': form,
    }
    context.update(extra_context or {})
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
