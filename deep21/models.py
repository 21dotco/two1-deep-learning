from django.db import models
from django.utils import timezone


class Token(models.Model):
    '''
        A model representing a token given to the user.
    '''

    created = models.DateTimeField(default=timezone.now)

    '''
        The value of the token, given to the user, which is a hashid of the
        database id.
    '''
    value = models.CharField(max_length=100, null=True, default=None)

    '''
        True when the token has successfully been redeemed, False otherwise.
    '''
    redeemed = models.BooleanField(default=False)
