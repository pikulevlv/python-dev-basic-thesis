# Generated by Django 2.2.2 on 2020-12-05 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recognition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='media/', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='tool',
            name='weights',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл весов'),
        ),
    ]
