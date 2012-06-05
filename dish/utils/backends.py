from dish.models import Account 


class ModelBackend(object):
    """
    Authenticates against django.contrib.auth.models.User.
    """
    # TODO: Model, login attribute name and password attribute name should be
    # configurable.
    def authenticate(self, username=None, password=None):
        try:
            account = Account.objects.get(username=username)
            if account.check_password(password):
                return account
        except Account.DoesNotExist:
            return None

    def get_user(self, account_id):
        try:
            return Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            return None

