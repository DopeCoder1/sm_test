from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, email, password, is_admin=False, **extra_fields):
        from user.models import AbstractUser

        """
        Create and save a user with the given email and password.
        """
        email = self.normalize_email(email)
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        if is_admin:
            user.roles = [AbstractUser.UserRolesEnum.ADMIN.value]
        else:
            user.roles = [AbstractUser.UserRolesEnum.USER.value]
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, is_admin=False, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, is_admin, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user( email, password, **extra_fields)