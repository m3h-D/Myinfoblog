# Generated by Django 2.2.6 on 2019-12-08 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='media/posts/img/%Y/%m/%d', verbose_name='تصویر عنوان'),
        ),
    ]