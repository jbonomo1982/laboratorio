# Generated by Django 2.0.13 on 2019-09-22 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documentos', '0008_auto_20190922_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parte_doc',
            name='documento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentos.Documento'),
        ),
    ]