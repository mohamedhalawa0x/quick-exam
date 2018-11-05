from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, EmailValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django_countries.fields import CountryField
from django.utils import timezone
from .utils import code_generator
from django.db.models.signals import post_save
from django.core.mail import send_mail

# Create your models here.

ALPHABETS_REGEX = r'^[a-zA-Z][a-zA-Z ]+$'
PHONE_REGEX = r'\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$'


class UserManager(BaseUserManager):
    def create_user(self,
                    email,
                    full_name,
                    date_of_birth,
                    country,
                    address,
                    phone_number,
                    password=None):
        """
        CCreates and saves a user with the given email, date of
        birth,country, address, phone_number, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            date_of_birth=date_of_birth,
            country=country,
            address=address,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, date_of_birth, country,
                         address, phone_number, password):
        """
        Creates and saves a superuser with the given email, date of
        birth,country, address, phone_number,  and password.
        """
        user = self.create_user(
            email,
            full_name,
            date_of_birth,
            country,
            address,
            phone_number,
            password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    # Email Address Field
    email = models.EmailField(
        verbose_name='Email Address',
        max_length=255,
        unique=True,
        validators=[
            EmailValidator(
                message="Invalid Email Address", code="invalid_email")
        ])

    # Full Name Field
    full_name = models.CharField(
        verbose_name="Full Name",
        max_length=255,
        validators=[
            MaxLengthValidator(255, "the provided name is too long"),
            RegexValidator(
                regex=ALPHABETS_REGEX,
                message="the full name should contain alphabets only.",
                code="invalid_name")
        ])

    # Country
    country = CountryField()

    # Street Address
    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Street Address")

    # Phone number
    phone_number = models.CharField(
        verbose_name="Phone Number",
        blank=True,
        max_length=15,
        validators=[
            RegexValidator(
                regex=PHONE_REGEX,
                message="Invalid Phone number",
                code="invalid_phone_number")
        ])

    # Date of birth
    date_of_birth = models.DateField()

    # is active: email
    is_active = models.BooleanField(default=True)

    # is admin
    is_admin = models.BooleanField(default=False)

    # Required Fields
    REQUIRED_FIELDS = [
        'full_name', 'country', 'date_of_birth', 'address', 'phone_number'
    ]
    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    # Get Full Name
    def get_username(self):
        return self.full_name

    # user has permission
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class EmailActivation(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    key = models.CharField(max_length=120)
    expired = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.key = code_generator()
        super(EmailActivation, self).save(*args, **kwargs)


def post_save_activation_reciever(sender, instance, created, *args, **kwargs):
    if created:
        try:
            url = "http://127.0.0.1:8000/identity/activate/" + instance.key
            # send email
            subject = " QuickExam - Email Activation"
            msg = "Kindly click the following hyperlink:\n" + url
            efrom = "quickexambeta@gmail.com"
            eto = instance.user.email
            send_mail(
                subject,
                msg,
                efrom,
                [eto],
                fail_silently=False,
            )
        except Exception as e:
            print(e)


post_save.connect(post_save_activation_reciever, sender=EmailActivation)


def post_save_user_model_reciever(sender, instance, created, *args, **kwargs):
    if created:
        try:
            EmailActivation.objects.create(user=instance)
        except Exception as e:
            pass


post_save.connect(
    post_save_user_model_reciever, sender=settings.AUTH_USER_MODEL)
