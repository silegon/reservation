#coding:utf-8
from dish.models import Account, Restaurant, Food, Order, PayRecord
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
    list_display = (  'username', 'real_name', 'need','need_lunch', 'need_dinner',  'balance') 
    search_fields = ['username', 'real_name']
    list_filter = ('need','need_lunch', 'need_dinner')
    actions = ['activation_need', 'stop_need', 'activation_need_lunch', 'stop_need_lunch', 'activation_need_dinner', 'stop_need_dinner' ]

    def activation_need(self, request, queryset):
        queryset.update(need=True)
    activation_need.short_description = u'激活用户点餐权限'

    def stop_need(self, request, queryset):
        queryset.update(need=False)
    stop_need.short_description = u'停止用户点餐权限'

    def activation_need_lunch(self, request, queryset):
        queryset.update(need_lunch=True)
    activation_need_lunch.short_description = u'需要中餐'

    def stop_need_lunch(self, request, queryset):
        queryset.update(need_lunch=False)
    stop_need_lunch.short_description = u'不需要中餐'

    def activation_need_dinner(self, request, queryset):
        queryset.update(need_dinner=True)
    activation_need_dinner.short_description = u'需要晚餐'

    def stop_need_dinner(self, request, queryset):
        queryset.update(need_dinner=False)
    stop_need_dinner.short_description = u'不需要晚餐'

class FoodInline(admin.TabularInline):
    model = Food
    extra = 30

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'exist',  'telephone', 'address', 'remark')
    search_fields = ['name', 'telephone', 'telephone', 'address', 'remark']
    inlines = [
        FoodInline,
    ]

class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'exist','restaurant', 'price')
    list_editable = ('price',)
    search_fields = ['restaurant__name','name']
    list_filter = ('exist', 'restaurant')
    actions = ['food_exist', 'food_inexist', 'pass_user_food']

    def food_inexist(self, request, queryset):
        queryset.update(exist=False)
    food_inexist.short_description = u'食物不可以预订'

    def food_exist(self, request, queryset):
        queryset.update(exist=True)
    food_exist.short_description = u'食物可以预订'

    def pass_user_food(self, request, queryset):
        for food in queryset:
            if ':' in food.name:
                food.name = food.name.split(':')[1]
                food.save()
    pass_user_food.short_description = u'用户提交的食物通过验证'

class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'username', 'restaurant', 'food', 'price', 'date',
                    'character', 'order_time', 'remark', 'status')
    list_editable = ('remark',)
    list_filter = ('status', 'restaurant','date' )

    actions = ['finish_order']

    # for test
    def finish_order(self, request, queryset):
        queryset.update(status='f')
    finish_order.short_description = u'完成订单'

class PayRecordAdmin(admin.ModelAdmin):
    list_display = ('account', 'date', 'cid' ,'bill')
    list_filter = ('account', 'date')

admin.site.register(Account, AccountAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(PayRecord, PayRecordAdmin)
