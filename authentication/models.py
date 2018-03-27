from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    name = models.CharField(max_length=40, blank=True)
    is_admin = models.BooleanField(default=False)
    is_gsec = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def get_name(self):
        return self.name
