# Generated by Django 4.1.4 on 2022-12-09 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestiondesstock', '0005_alter_materiels_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materiels',
            name='image',
            field=models.ImageField(null=True, upload_to='media/upload'),
        ),
    ]
