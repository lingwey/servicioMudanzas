# Generated by Django 5.2.3 on 2025-06-18 07:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('registro_vehiculo', models.CharField(blank=True, max_length=50, null=True)),
                ('empresa_certificaciones', models.TextField(blank=True, null=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
