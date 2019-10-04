# Generated by Django 2.0.13 on 2019-08-19 23:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_nc', '0002_auto_20190715_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivo',
            name='archivo',
            field=models.FileField(upload_to='archivos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpeg', 'jpg', 'png', 'gif'])]),
        ),
    ]