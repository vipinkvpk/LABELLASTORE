from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
  
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(max_length=20,unique=False,verbose_name='phone number',
                             blank=True,null=True, help_text='enter 10 digit phone number')
    username = models.CharField(max_length=20,unique=False,verbose_name='username',
                             blank=True,null=True,)

    wallet  = models.PositiveIntegerField(default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = CustomUserManager()




# class UserOTP(models.Model):
#     user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
#     time_st=models.DateTimeField(auto_now=True)
#     otp=models.IntegerField()


from django.db import models
from django.utils import timezone

class UserOTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    time_st = models.DateTimeField(auto_now_add=True)  # Use auto_now_add
    otp = models.IntegerField()
    expiry_time = models.DateTimeField()  # Add expiry time
    is_valid = models.BooleanField(default=True)  # Track OTP validity

    def save(self, *args, **kwargs):
        # Set expiry time on creation
        if not self.id:  # Only if a new object
            self.expiry_time = timezone.now() + timezone.timedelta(seconds=60) # Set expiry to 5 minutes from now
        super(UserOTP, self).save(*args, **kwargs)
