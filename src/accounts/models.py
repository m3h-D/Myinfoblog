from django.db import models
from django.core.validators import RegexValidator
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model

User = get_user_model()


# # Create your models here.

# class UserManager(BaseUserManager):

#     def create_user(self, email, phone, password=None, **extra_fields):
#         """create and saves a new user"""
#          if not email:
#              raise ValueError('Users must have an email address')
#          if not phone:
#              raise ValueError('Users must have an phone number')
#         user = self.model(
#             email=self.normalize_email(email), **extra_fields)  # extra_fields baraye ezafe kardane field haye jadide
#         # passowd o nemishud tu khate bala guzasht chun bayad encript she
#         user.set_password(password)
#         user.save(using=self._db) #

#         return user

# def create_superuser(self, email, phone, password):
#     """
#     Creates and saves a superuser with the given email, date of
#     birth and password.
#     """
#     user = self.create_user(
#         email,
#         password=password,
#         phone=phone,
#     )
#     user.is_admin = True
#     user.save(using=self._db)
#     return user


# class User(AbstractBaseUser, PermissionsMixin):
#     """custome User model e ke beja username az email baraye login estefade mikone"""

#     email = models.EmailField(
#         max_length=255, unique=True, verbose_name='ایمیل')
#     phone_reg = RegexValidator(regex=r'[0][9][0-9]{9,9}$')
#     phone = models.CharField(
#         validators=[phone_reg],
#         max_length=11,
#         blank=True,
#         verbose_name='شماره تلفن'
#     )
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_admin = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     # REQUIRED_FIELDS = ['phone']
#     def __str__(self):
#       return self.email


# def has_perm(self, perm, obj=None):
#     "Does the user have a specific permission?"
#     # Simplest possible answer: Yes, always
#     return True

# def has_module_perms(self, app_label):
#     "Does the user have permissions to view the app `app_label`?"
#     # Simplest possible answer: Yes, always
#     return True

# @property
# def is_staff(self):
#     "Is the user a member of staff?"
#     # Simplest possible answer: All admins are staff
#     return self.is_admin


class City(models.Model):
    """modele Ostan"""
    name = models.CharField(max_length=120, verbose_name='نام استان')

    def __str__(self):
        return self.name


class Town(models.Model):
    """model e shahr ke ba city(ostan) relationship dare"""
    name = models.CharField(max_length=120, verbose_name='نام شهر')
    city = models.ForeignKey(City, related_name='town',
                             on_delete=models.CASCADE, verbose_name='نام استان')

    def __str__(self):
        return self.name


class Profile(models.Model):
    """profile baraye har user"""
    user = models.OneToOneField(
        User, related_name="profile", on_delete=models.CASCADE, verbose_name="نام کاربری")
    first_name = models.CharField(
        max_length=100, blank=True, verbose_name="نام")
    last_name = models.CharField(
        max_length=100, blank=True, verbose_name="نام خانوادگی")
    bio = models.CharField(max_length=500, blank=True,
                           verbose_name='درباره من')
    date_of_birth = models.DateField(
        blank=True, verbose_name="تاریخ تولد", null=True)
    # city = models.CharField(max_length=30, blank=True, verbose_name='شهر')
    town = models.ForeignKey(
        Town, related_name='profile', blank=True, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(
        City, related_name='profile', blank=True, null=True, on_delete=models.CASCADE)
    address = models.CharField(
        max_length=1000, blank=True, verbose_name='ادرس')
    phone_reg = RegexValidator(regex=r'[0][9][0-9]{9,9}$')
    phone = models.CharField(
        validators=[phone_reg],
        max_length=11,
        blank=True,
        verbose_name='شماره تلفن'
    )
    post_code = models.CharField(
        max_length=20, blank=True, verbose_name='کدپستی')
    image = models.ImageField(
        blank=True, upload_to='users_profile/img/%Y-%m-%d', verbose_name='اواتار')

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = "پروفایل ها"

    def __str__(self):
        return "پروفایل {}".format(self.user.username)
