# Generated by Django 4.1.3 on 2023-06-18 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioncouriers', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date_lecture',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='fil_de_discussion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestioncouriers.message'),
        ),
        migrations.AddField(
            model_name='message',
            name='lu',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='message',
            name='notification_email_envoyee',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_envoie',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='objet',
            field=models.CharField(max_length=200),
        ),
    ]
