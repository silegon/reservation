# -*- coding:utf-8 -*-
from django import forms
from dish.utils.auth import authenticate
from dish.models import Account

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(label="用户名", max_length=30)
    password = forms.CharField(label="密码", widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.account_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.account_cache = authenticate(username=username, password=password)
            if self.account_cache is None:
                raise forms.ValidationError("请输入正确的用户名和密码")
            if self.account_cache.need == False:
                raise forms.ValidationError("请联系前台开通订餐权限")
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError("您的浏览器未开启cookie,cookie是登陆后台所必须的")

    def get_user_id(self):
        if self.account_cache:
            return self.account_cache.id
        return None

    def get_user(self):
        return self.account_cache

class PasswordMailForm(forms.Form):
    username = forms.CharField(label="用户名")
    email = forms.EmailField(label="邮箱地址")

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if username and email:
            account = Account.objects.get(username=username)
            if account:
                if account.email != email:
                    raise forms.ValidationError("账号和邮箱不匹配")
            else:
                raise forms.ValidationError("没有该账号")
        return self.cleaned_data
