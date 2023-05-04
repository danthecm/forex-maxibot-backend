from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import hashers
from helpers.api_key import generate_api_key, verify_api_key


class CustomUserManager(BaseUserManager):
    # Add custom methods and behavior here

    def create_user(self, username, email, password):
        if not email:
            raise ValueError("User must have an email")
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        if not email:
            raise ValueError("User must have an email")
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save()
        return user


class User(AbstractBaseUser):
    # Add custom fields and methods here

    username = models.CharField(max_length=225, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verification_code = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "password"]

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name is not None and self.last_name is not None else "User"

    @property
    def get_short_name(self):
        return self.first_name if self.first_name is not None else "User"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class ApiKeyModel(models.Model):
    user = models.ForeignKey(
        User, related_name="api_keys", on_delete=models.CASCADE)
    key = models.CharField(max_length=225,)
    name = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.pk:
            raw_key, harsed_key = generate_api_key()
            self.key = harsed_key
        super().save(*args, **kwargs)
        return raw_key

    @classmethod
    def verify(cls, raw_key):
        api_keys = cls.objects.all()
        for api_key in api_keys:
            if verify_api_key(raw_key, api_key.key):
                return api_key
        return None

    def __str__(self) -> str:
        return f"{self.user.username} {self.name}"


class DateAbtract(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TradeProfile(models.Model):
    user = models.ForeignKey(
        User, related_name="trade_profile", on_delete=models.CASCADE)
    mt5_login = models.IntegerField(unique=True)
    mt5_password = models.CharField(max_length=150)
    mt5_server = models.CharField(max_length=200)


class BotModel(DateAbtract):
    profile = models.ForeignKey(
        TradeProfile, related_name="bots", on_delete=models.CASCADE)
    symbol = models.CharField(max_length=200)
    volume = models.DecimalField(decimal_places=2, max_digits=4)
    grid_interval = models.IntegerField()
    take_profit = models.IntegerField()
    status = models.CharField(max_length=100)
    close_trade = models.IntegerField()
    pip_margin = models.DecimalField(decimal_places=2, max_digits=4)
    side = models.CharField(max_length=5, choices=(
        ("buy", "buy"), ("sell", "sell"), ("all", "all")), default="all")
    skip = models.DecimalField(decimal_places=5, max_digits=6, default=0)
    profit = models.DecimalField(decimal_places=4, max_digits=10, default=0)
    equity = models.DecimalField(decimal_places=4, max_digits=20, default=0)
    profit_margin = models.DecimalField(
        decimal_places=4, max_digits=20, default=50)
    min_combo = models.DecimalField(
        decimal_places=4, max_digits=20, default=0.5)

    def __str__(self):
        return f"{self.owner.username} {self.symbol}"


class OrderModel(DateAbtract):
    bot = models.ForeignKey(
        BotModel, related_name="orders", on_delete=models.CASCADE)
    order_id = models.IntegerField()
    price = models.DecimalField(decimal_places=5, max_digits=10)
    type = models.CharField(max_length=10, choices=(
        ("buy", "buy"), ("sell", "sell"), ("deposit", "deposit"), ("withdrawal", "withdrawal")))
    take_profit = models.DecimalField(decimal_places=5, max_digits=10)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.type
