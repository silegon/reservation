#coding:utf-8
from collections import defaultdict
import hashlib
import datetime
import random
from django.db import models
from django.utils.encoding import smart_str

import logging
logger = logging.getLogger('test')

def get_hexdigest(salt, raw_password):
    raw_password, salt = smart_str(raw_password), smart_str(salt)
    return hashlib.sha224(salt + raw_password).hexdigest()

class AccountManager(models.Manager):
    def create_user(self, username, real_name, password, balance=0.00):
        try:
            account = Account.objects.get(username=username)
            return False
        except Account.DoesNotExist:
            account = self.model(username=username, real_name=real_name, balance=balance)
            account.set_password(password)
            account.save(using=self._db)
            return account

    def need_service(self, dish_character):
        accounts = Account.objects.filter(need=True)

        if dish_character == 'l':
            available_accounts = accounts.filter(need_lunch=True)
        else:
            available_accounts = accounts.filter(need_dinner=True)

        need_service_accounts = map(lambda x:x['real_name'], available_accounts.values('real_name'))
        return need_service_accounts

class Account(models.Model):
    username = models.CharField(max_length=20, unique=True, db_index=True, verbose_name="用户名")
    real_name = models.CharField(max_length=20, db_index=True, verbose_name="真实姓名")
    password = models.CharField(max_length=61, help_text="使用 '[salt]$[hexdigest]' ", verbose_name="密码")
    balance = models.FloatField(blank=True, verbose_name = "余额")
    need = models.BooleanField(default=False, verbose_name = "提供订餐服务")
    need_lunch = models.BooleanField(default=False, verbose_name = "需要中餐")
    need_dinner = models.BooleanField(default=False, verbose_name = "需要晚餐")
    objects = AccountManager()

    class Meta:
        verbose_name_plural = "用户账号"

    def is_authenticated(self):
        return True

    def __unicode__(self):
        return '%s'%(self.real_name)

    def pay(self, amount):
        if amount >= 0:
            self.balance -= amount 
            self.save()
        else:
            raise "amount can not negative number"

    def set_password(self, raw_password):
        salt = get_hexdigest(str(random.random()), str(random.random()))[:4]
        password = salt + '$' + get_hexdigest(salt, raw_password) 
        self.password = password
        self.save()

    def check_password(self, raw_password):
        salt, enc_password = self.password.split('$')
        return get_hexdigest(salt, raw_password) == enc_password 

class AnonymousAccount(object):

    def __unicode__(self):
        return 'AnonymousUser'

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __init__(self):
        pass

    def is_authenticated(self):
        return False

class Restaurant(models.Model):
    name = models.CharField(max_length=50, verbose_name="餐馆名")
    telephone = models.CharField(max_length=20, verbose_name="电话")
    address = models.CharField(max_length=100, verbose_name="地址")
    update = models.DateField(auto_now_add=True, verbose_name="菜单更新日期")
    remark = models.TextField(blank=True, verbose_name="备注")
    exist = models.BooleanField(default=True, verbose_name="提供服务")

    def __str__(self):
        return self.name.encode('utf-8')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "外卖服务提供商"

class Food(models.Model):
    name = models.CharField(max_length=50, verbose_name="食物名")
    restaurant = models.ForeignKey('Restaurant', db_index=True, on_delete=models.PROTECT, verbose_name="餐馆名")
    price = models.FloatField(verbose_name="价格")
    exist = models.BooleanField(default=True, verbose_name="是否供应")

    def __str__(self):
        return self.name.encode('utf-8')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "食物"


class OrderManager(models.Manager):
    def create_order(self, account, food_id, date, dish_character, remark):
        try:
            food = Food.objects.get(pk=food_id)
            order = Order(username=account, restaurant=food.restaurant, food=food,
                          price=food.price, date=date, character=dish_character,
                          remark=remark)
            order.save()
        except:
            return False
        return order

    def order_booked(self, account):
        return Order.objects.filter(username=account, status='b').order_by('-date', '-character')

    def order_confirmed(self, account):
        return Order.objects.filter(username=account, status='c').order_by('-date', '-character')

    def order_finished(self, account):
        return Order.objects.filter(username=account, status='f').order_by('-date', '-character')

    def get_process_order(self, date, dish_character, status='b'):
        query = Order.objects.filter(date=date, character=dish_character, 
                                     status=status).order_by('food')
        item_list = []
        for item in query:
            item_list.append({'pk':item.pk, 
                              'username':item.username.real_name, 
                              'restaurant':item.restaurant.name + 'tel:' + 
                              item.restaurant.telephone,
                              'food_name':item.food.name, 
                              'price':item.price, 
                              'remark':item.remark, 
                              'status':item.status})
            return item_list

    def confirm_orders(self, order_id_list):
        result=[]
        for order_id in order_id_list:
            try:
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                result.append(order_id)
                if order:
                    if order.status == 'b':
                        order.status = 'c'
                        order.save()
                    else:
                        result.append(order_id)
                        if result:
                            return ','.join(result)
        return 'Success'

    def finish_orders(self, order_id_list):
        result=[]
        for order_id in order_id_list:
            try:
                order = Order.objects.get(pk=order_id)
            except Order.DoesNotExist:
                result.append(order_id)
                if order:
                    if order.status == 'c':
                        order.status = 'f'
                        order.save()
                    else:
                        result.append(order_id)
                        if result:
                            return ','.join(result)
        return 'Success'


class Order(models.Model):

    ORDER_CHARACTER = (
        ('l','中餐'), #Lunch
        ('d','晚餐'), #Dinner
    ) 
    ORDER_STATUS = (
        ('b','预订'), #Book
        ('c','确认'), #Confirm
        ('f','完成'), #Finish
        ('a','取消'), #cAncle
    ) 

    username = models.ForeignKey('Account',db_index=True, on_delete=models.PROTECT, verbose_name="用户名")
    restaurant = models.ForeignKey('Restaurant', on_delete=models.PROTECT, verbose_name="餐馆名")
    food = models.ForeignKey('Food', on_delete=models.PROTECT, verbose_name="食物名")
    price = models.FloatField(verbose_name="价格")
    date = models.DateField(db_index=True, verbose_name="日期")
    character = models.CharField(max_length=1, choices=ORDER_CHARACTER, verbose_name="餐特征")
    order_time = models.DateTimeField(auto_now_add=True, verbose_name="订单时间")
    remark = models.CharField(max_length=50, blank=True, verbose_name="备注")
    status = models.CharField(max_length=1, choices=ORDER_STATUS, verbose_name="餐状态", default='b')
    pay = models.BooleanField(default=False)
    objects = OrderManager()

    class Meta:
        verbose_name_plural = "订单"

    def dish_character(self):
        if self.character=='l':
            return u'中餐'
        else:
            return u'晚餐'

    def __unicode__(self):
        return u'%s,%s,%s,%s,%s'%(self.username, self.date, self.character, self.food, self.restaurant)

    def __str__(self):
        return '%s'%self.food 

def pay_dish(interval, character, subsidy):
    yestoday = datetime.date.today() - datetime.timedelta(1)
    bmonth = yestoday - datetime.timedelta(interval)
    trading_days = Order.objects.filter(date__lte=yestoday, date__gte=bmonth, character=character, status='f', pay=False).values('date').distinct()
    if trading_days:
        for _sday in trading_days:
            sday = _sday.values()[0]
            orders = Order.objects.filter(date=sday, character=character, status='f', pay=False)
            d_costs = defaultdict(list)
            for order in orders:
                d_costs[order.username.pk].append(order.price)
                order.pay=True
                order.save()

            for key in d_costs.keys():
                user = Account.objects.get(pk=key)
                amount = reduce(lambda x,y:x+y, d_costs[key])
                bill = amount - subsidy
                bill = bill if bill > 0 else 0
                user.pay(bill)# lunch subsidy
                pay_record = PayRecord(account=user, date=sday, cid=character, bill=bill)
                pay_record.save()

class PayRecordManager(models.Manager):
    def finish_pay(self):
        settlement = True
        pay_dish(30, 'l', 8) # check_interval, dish character,dish subsidy
        pay_dish(30, 'd', 15)
        return settlement

class PayRecord(models.Model):
    account = models.ForeignKey('Account', on_delete=models.PROTECT, verbose_name='账号')
    date = models.DateField(verbose_name="日期")
    cid = models.CharField(max_length=1, choices=Order.ORDER_CHARACTER, verbose_name="餐特征")
    bill = models.FloatField(verbose_name="扣费金额")
    objects = PayRecordManager()

    def dish_character(self):
        if self.cid=='l':
            return u'中餐'
        else:
            return u'晚餐'

    class Meta:
        verbose_name_plural = "扣费记录"

    def __unicode__(self):
        return "%s,%s,%s,%s"%(self.account.real_name, self.date, self.cid, self.bill)
