from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import settings
from autoslug import AutoSlugField

from watchobb.managers import MyUserManager


# Create your models here.
class Company(models.Model):
    comp_name = models.CharField(max_length=255, unique=True)
    comp_add = models.CharField(max_length=255)
    comp_email = models.EmailField()
    industry_id = models.PositiveIntegerField()
    employees = models.IntegerField()
    comp_mob = models.PositiveBigIntegerField()
    comp_type_choice = (
        ('Product Based', 'Product Based'),
        ('Service Based', 'Service Based'),
        ('Startup', 'Startup'),
        ('E-Commerce', 'E-Commerce'),
    )
    comp_type = models.CharField(choices=comp_type_choice, default='product', null=False, max_length=50)
    comp_desc = models.TextField(default="xyz")
    slug = AutoSlugField(populate_from = 'comp_name', unique = True, slugify=lambda value: value.replace(' ','_'))

    class Meta:
        db_table = 'company'

    def __str__(self):
        return self.comp_name

    def get_absolute_url(self):
        return "/details/{}".format(self.slug)

class Industry(models.Model):
    industry = models.CharField(max_length=255)

    class Meta:
        db_table = 'industry'

    def __str__(self):
        return self.industry

class Vacancy(models.Model):
    job_profile = models.CharField(max_length=255)
    keyword_id = models.IntegerField()
    job_description = models.TextField()
    experience = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=40)
    salary = models.PositiveIntegerField()
    recruiter_id = models.PositiveIntegerField()
    comp_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_posted = models.DateTimeField()
    date_expired = models.DateTimeField()
    isactive = models.BooleanField()
    industry_id = models.PositiveIntegerField()
    job_type_choices = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Project', 'Project'),
        ('Intership', 'Intership'),
    )
    job_type = models.CharField(choices=job_type_choices, default='1', null=False, max_length=255)
    work_type_choices = (
        ('Work From Home', 'Work From Home'),
        ('Work From Office', 'Work From Office'),
        ('Hybrid', 'Hybrid'),
    )
    work_from = models.CharField(choices=work_type_choices,default='office', null=False, max_length=255)

    class Meta:
        db_table ='vacancy'

    def __str__(self):
        return self.job_profile
        
class Recruiter(models.Model):
    comp_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    recruiter_name = models.CharField(max_length=255)
    recruiter_email = models.EmailField()
    recruiter_mob = models.PositiveBigIntegerField()

    class Meta:
        db_table = 'recruiter'

    def __str__(self):
        return self.recruiter_name


class MyUser(AbstractBaseUser, PermissionsMixin):
    email            = models.EmailField(max_length=254, unique=True, verbose_name='email address')
    
    is_staff         = models.BooleanField(default=False)
    is_superuser     = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_recruiter     = models.BooleanField(default=False)
    last_login       = models.DateTimeField(auto_now=True)
    date_joined      = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)


class Profile(models.Model):
    user             = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname        = models.CharField(max_length=80, null=True)
    lastname         = models.CharField(max_length=80, null=True)
    gender_choice    = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender           = models.CharField(max_length=6,choices=gender_choice,default='Male',null=True)
    date_of_birth    = models.DateField(null=True)
    phone            = PhoneNumberField(null=True,)
    high_school      = models.CharField(max_length=255, null=True)
    hs_year          = models.PositiveIntegerField(null=True)
    hs_marks         = models.DecimalField(max_digits=4,decimal_places=2,null=True)
    inter            = models.CharField(max_length=255, null=True)
    inter_year       = models.PositiveBigIntegerField(null=True)
    inter_marks      = models.DecimalField(max_digits=4,decimal_places=2,null=True)  
    exp_years        = models.SmallIntegerField(null=True)
    job_profile      = models.CharField(max_length=100, null=True)
    projects         = models.TextField(null=True)
    curr_company     = models.CharField(max_length=255, null=True)
    curr_salary      = models.PositiveBigIntegerField(null=True)
    expect_salary    = models.PositiveBigIntegerField(null=True)
    resume           = models.FileField(null=True)
    # slug             = AutoSlugField(populate_from='user', unique=True)

    # def get_absolute_url(self):
    #     return "/profile/{}".format(self.slug)

    class Meta:
        db_table     = 'profile'

    def __str__(self):
        return self.user.email
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
