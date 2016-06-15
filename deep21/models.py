from django.db import models
from django.utils import timezone


class Request(models.Model):
    '''
        A model representing a single request from a user.
    '''

    created = models.DateTimeField(default=timezone.now)

    '''
        A token given to the user, a hashid of the database id,
        which is also used to name files on S3, etc.
    '''
    token = models.CharField(max_length=100, null=True, default=None)

    '''
        The server filepath for output image to store temporarily between
        fetching from s3 and uploading to imgur.
    '''
    output_filepath = models.CharField(max_length=150, null=True)

    '''
        The name of the output file on S3.
    '''
    output_s3_filename = models.CharField(max_length=150, null=True)

    '''
        True when the token has successfully been redeemed, False otherwise.
    '''
    redeemed = models.BooleanField(default=False)
