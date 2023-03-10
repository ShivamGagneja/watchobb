# Generated by Django 4.1.5 on 2023-01-17 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comp_name', models.CharField(max_length=255)),
                ('comp_add', models.CharField(max_length=255)),
                ('comp_email', models.EmailField(max_length=254)),
                ('industry_id', models.PositiveIntegerField()),
                ('employees', models.IntegerField()),
                ('comp_mob', models.PositiveBigIntegerField()),
                ('comp_type', models.CharField(choices=[('Product Based', 'Product Based'), ('Service Based', 'Service Based'), ('Startup', 'Startup'), ('E-Commerce', 'E-Commerce')], default='product', max_length=50)),
                ('comp_desc', models.TextField(default='xyz')),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('industry', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'industry',
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_profile', models.CharField(max_length=255)),
                ('keyword_id', models.IntegerField()),
                ('job_description', models.TextField()),
                ('experience', models.PositiveSmallIntegerField()),
                ('location', models.CharField(max_length=40)),
                ('salary', models.PositiveIntegerField()),
                ('recruiter_id', models.PositiveIntegerField()),
                ('date_posted', models.DateTimeField()),
                ('date_expired', models.DateTimeField()),
                ('isactive', models.BooleanField()),
                ('industry_id', models.PositiveIntegerField()),
                ('job_type', models.CharField(choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time'), ('Project', 'Project'), ('Intership', 'Intership')], default='1', max_length=255)),
                ('work_from', models.CharField(choices=[('Work From Home', 'Work From Home'), ('Work From Office', 'Work From Office'), ('Hybrid', 'Hybrid')], default='office', max_length=255)),
                ('comp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='watchobb.company')),
            ],
            options={
                'db_table': 'vacancy',
            },
        ),
        migrations.CreateModel(
            name='Recruiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recruiter_name', models.CharField(max_length=255)),
                ('recruiter_email', models.EmailField(max_length=254)),
                ('recruiter_mob', models.PositiveBigIntegerField()),
                ('comp_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='watchobb.company')),
            ],
            options={
                'db_table': 'recruiter',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=80, null=True)),
                ('lastname', models.CharField(max_length=80, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=6, null=True)),
                ('date_of_birth', models.DateField(null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None)),
                ('high_school', models.CharField(max_length=255, null=True)),
                ('hs_year', models.PositiveIntegerField(null=True)),
                ('hs_marks', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('inter', models.CharField(max_length=255, null=True)),
                ('inter_year', models.PositiveBigIntegerField(null=True)),
                ('inter_marks', models.DecimalField(decimal_places=2, max_digits=4, null=True)),
                ('exp_years', models.SmallIntegerField(null=True)),
                ('job_profile', models.CharField(max_length=100, null=True)),
                ('projects', models.TextField(null=True)),
                ('curr_company', models.CharField(max_length=255, null=True)),
                ('curr_salary', models.PositiveBigIntegerField(null=True)),
                ('expect_salary', models.PositiveBigIntegerField(null=True)),
                ('resume', models.FileField(null=True, upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
    ]
