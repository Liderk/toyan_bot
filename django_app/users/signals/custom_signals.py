import django.dispatch

__all__ = ('telegram_user_accepted',)

"""
providing_args=['instance']
"""
telegram_user_accepted = django.dispatch.Signal()
