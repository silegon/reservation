from django.conf import settings

DISH_AUTHENTICATION_BACKENDS = getattr(settings,'DISH_AUTHENTICATION_BACKENDS',('dish.utils.backends.ModelBackend',))
REDIRECT_FIELD_NAME = getattr(settings, 'DISH_REDIRECT_FIELD_NAME', 'next')
# lunch type = 'l'
# dinner type = 'd'

# book
# cancel
# confirm
# finish
