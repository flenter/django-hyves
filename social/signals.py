"""signals for the social app
"""
from django.dispatch import Signal

social_user_authenticated = Signal(providing_args=["user", "access_token"])
