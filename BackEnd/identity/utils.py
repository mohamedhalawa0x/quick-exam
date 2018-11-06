import random
import string

from django.conf import settings

#SHORTCODE_MIN can be placed in settings.py
SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 15)


def code_generator(size=SHORTCODE_MIN,
                   chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for c in range(size))
