# Generated by Django 4.1.3 on 2022-12-13 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionprojets', '0009_alter_projet_pieces_jointes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projet',
            name='pieces_jointes',
            field=models.FileField(null=True, upload_to='media/upload/documents', verbose_name='image'),
        ),
    ]