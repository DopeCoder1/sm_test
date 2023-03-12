from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.postgres.fields import ArrayField
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from user.managers import CustomUserManager
from django.db import models


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    class UserRolesEnum(models.TextChoices):
        ADMIN = 'ADMIN',
        USER = 'USER'

    class GenderChoices(models.TextChoices):
        MALE = 'MALE'
        FEMALE = 'FEMALE'

    class CurrencyChoices(models.TextChoices):
        tenge = 'тенге'
        ruble = 'рубль'
        dollar = 'доллар'
        euro = 'евро'

    phone_number = models.CharField(
        _("phone number"),
        validators=[RegexValidator(regex=r"^\+?77(\d{9})$",
                                   message=_("Неправильный номер телефона"))],
        max_length=50,
        unique=True,
        null=True
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True, null=True)
    code = models.CharField(blank=True, null=True, max_length=6)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_secure = models.BooleanField(_("secure"), default=False)
    roles = ArrayField(models.CharField(max_length=20, choices=UserRolesEnum.choices), default=list, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    birthdate = models.DateField(_("Date"), null=True, blank=True)
    image = models.ImageField(upload_to='photos/', null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, null=True, blank=True)
    position = models.CharField(max_length=150, null=True, blank=True)
    IIN = models.CharField(max_length=12, null=True, blank=True)
    organization_name = models.CharField(max_length=150, null=True, blank=True)
    BIN = models.CharField(max_length=12, null=True, blank=True)
    BIK = models.CharField(max_length=8, null=True, blank=True)
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    IBAN = models.CharField(max_length=20, null=True, blank=True)
    kbe = models.CharField(max_length=2, null=True, blank=True)
    currency = models.CharField(max_length=10, choices=CurrencyChoices.choices, null=True, blank=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_role(self, role: UserRolesEnum):
        return role in self.roles

    def __str__(self) -> str:
        return f"{self.phone_number} - {self.email}"


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
