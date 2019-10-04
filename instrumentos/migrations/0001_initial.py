# Generated by Django 2.0.13 on 2019-09-22 17:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('documentos', '0008_auto_20190922_1426'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Instrumento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clase', models.CharField(choices=[('M', 'Medición'), ('A', 'Analítico'), ('O', 'Otro')], max_length=1)),
                ('nombre', models.CharField(help_text='Poner el nombre del instrumento si es referido en el documento, para que sea fácil encontrarlo', max_length=200)),
                ('codigo', models.CharField(default='Genérico', help_text='Poner el código del instrumento si es referido en el documento, para que sea fácil encontrarlo', max_length=200)),
                ('descripcion', models.TextField()),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sector', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='documentos.Sector')),
            ],
        ),
        migrations.CreateModel(
            name='Relacion_instr_doc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documentos.Categoria_doc')),
                ('instrumento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='instrumentos.Instrumento')),
            ],
        ),
    ]