# Generated by Django 2.2.5 on 2019-10-10 19:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='نام استان')),
            ],
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='نام شهر')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='town', to='accounts.City', verbose_name='نام استان')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=100, verbose_name='نام خانوادگی')),
                ('bio', models.CharField(blank=True, max_length=500, verbose_name='درباره من')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('address', models.CharField(blank=True, max_length=1000, verbose_name='ادرس')),
                ('phone', models.CharField(blank=True, max_length=11, validators=[django.core.validators.RegexValidator(regex='[0][9][0-9]{9,9}$')], verbose_name='شماره تلفن')),
                ('post_code', models.CharField(blank=True, max_length=20, verbose_name='کدپستی')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='اواتار')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='accounts.City')),
                ('town', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='accounts.Town')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='نام کاربری')),
            ],
            options={
                'verbose_name': 'پروفایل',
                'verbose_name_plural': 'پروفایل ها',
            },
        ),
    ]
