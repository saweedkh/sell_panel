# Django Built-in modules
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, full_name, password, mobile_number=None, email=None):
        if not username:
            raise ValueError(_('کاربر باید نام کاربری داشته باشد.'))
        if not full_name:
            raise ValueError(_('کاربر باید نام داشته باشد.'))

        user = self.model(username=username, full_name=full_name, mobile_number=mobile_number,
                          email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, password):
        user = self.create_user(username, full_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
