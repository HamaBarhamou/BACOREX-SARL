# Generated by Django 4.1.3 on 2022-12-31 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionprojets', '0013_remove_task_list_intervenant_remove_task_attribuer_a_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='pieces_jointes',
            field=models.FileField(null=True, upload_to='media/upload/documents'),
        ),
    ]
