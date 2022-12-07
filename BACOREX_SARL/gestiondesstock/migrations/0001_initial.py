# Generated by Django 4.1.4 on 2022-12-07 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriMateriel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('description', models.CharField(default=None, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Materiels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('description', models.CharField(default=None, max_length=150)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestiondesstock.categorimateriel')),
            ],
        ),
    ]