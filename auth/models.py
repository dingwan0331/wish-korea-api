from django.db import models

from core.models import TimeStampModel

class User(TimeStampModel):
    username      = models.CharField(max_length = 50, unique = True)
    password      = models.BinaryField(max_length = 60)
    email         = models.CharField(max_length = 100, unique = True)
    phone_number  = models.CharField(max_length = 13, unique = True)
    name          = models.CharField(max_length = 5)
    address       = models.CharField(max_length = 200, null = True)
    nick_name     = models.CharField(max_length = 15, null = True)

    class Meta:
        db_table = 'users'