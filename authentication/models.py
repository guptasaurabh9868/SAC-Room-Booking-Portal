from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        account = self.model(
            email=self.normalize_email(email)
        )

        account.set_password(password)
        account.save()

        return account

    def create_superuser(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_admin = True
        account.save()

        return account

    def create_gsec_user(self, email, password, **kwargs):
        account = self.create_user(email, password, **kwargs)

        account.is_gsec = True
        account.save()

        return account
        
class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)

    name = models.CharField(max_length=40, blank=True)
    is_admin = models.BooleanField(default=False)
    is_gsec = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'

    def __unicode__(self):
        return self.email

    def get_name(self):
        return self.name