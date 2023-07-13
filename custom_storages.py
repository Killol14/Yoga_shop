from django.conf import settings
from django.backends.s3boto3 import s3Boto3Storage

class StatickStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION
