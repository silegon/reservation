#from django.conf import settings

#import datetime
from warnings import warn
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
#from django.contrib.auth.signals import user_logged_in, user_logged_out

SESSION_KEY = 'youease_platform_id'

def load_backend(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]

    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing authentication backend %s: "%s"' % (path, e))
    except ValueError, e:
        raise ImproperlyConfigured('Error importing authentication backends. Is DISH_AUTHENTICATION_BACKENDS a correctly defined list or tuple?')
    
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" authentication backend' % (module, attr))

    if not hasattr(cls, "supports_object_permissions"):
        warn("Authentication backends without a `supports_object_permissions` attribute are deprecated. Please define it in %s." % cls,
             DeprecationWarning)
        cls.supports_object_permissions = False

    if not hasattr(cls, 'supports_anonymous_user'):
        warn("Authentication backends without a `supports_anonymous_user` attribute are deprecated. Please define it in %s." % cls,
             DeprecationWarning)
        cls.supports_anonymous_user = False

    if not hasattr(cls, 'supports_inactive_user'):
        warn("Authentication backends without a `supports_inactive_user` attribute are deprecated. Please define it in %s." % cls,
             PendingDeprecationWarning)
        cls.supports_inactive_user = False
    return cls()

def get_backends():
    from dish.conf import dish_settings
    backends = []
    for backend_path in dish_settings.DISH_AUTHENTICATION_BACKENDS:
        backends.append(load_backend(backend_path))
    if not backends:
        raise ImproperlyConfigured('No authentication backends have been defined. Does DISH_AUTHENTICATION_BACKENDS contain anything?')
    return backends

def authenticate(**credentials):
    """
    If the given credentials are valid, return a User object.
    """
    for backend in get_backends():
        try:
            account = backend.authenticate(**credentials)
        except TypeError:
            # This backend doesn't accept these credentials as arguments. Try the next one.
            continue
        if account is None:
            continue
        # Annotate the user object with the path of the backend.
        account.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
        return account


def platform_login(request, account):
    """
    Persist a account id and a backend in the request. This way a account doesn't
    have to reauthenticate on every request.
    """
    if account is None:
        account = request.account
    # TODO: It would be nice to support different login methods, like signed cookies.
    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != account.id:
            if '_auth_user_id' in request.session:
                request.session.cycle_key()
            else:
                request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = account.id
    #request.session[BACKEND_SESSION_KEY] = account.backend
    if hasattr(request, 'account'):
        request.account = account
    #user_logged_in.send(sender=user.__class__, request=request, user=user)

def platform_logout(request):
    """
    Removes the authenticated account's ID from the request and flushes their
    session data.
    """
    # Dispatch the signal before the account is logged out so the receivers have a
    # chance to find out *who* logged out.
    account = getattr(request, 'account', None)
    if hasattr(account, 'is_authenticated') and not account.is_authenticated():
        account = None
    #user_logged_out.send(sender=user.__class__, request=request, user=user)

    request.session.flush()
    if hasattr(request, 'account'):
        from dish.models import AnonymousAccount
        request.account = AnonymousAccount()

def get_youease_account(request):
    from dish.models import Account, AnonymousAccount
    try:
        account_id = request.session[SESSION_KEY]
        try:
            return Account.objects.get(pk=account_id)
        except Account.DoesNotExist:
            return AnonymousAccount()
    except KeyError:
        return AnonymousAccount()
