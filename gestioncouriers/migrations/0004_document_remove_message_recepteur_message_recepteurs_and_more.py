# Generated by Django 4.1.3 on 2023-06-18 20:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestioncouriers', '0003_message_date_lecture_message_fil_de_discussion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='message',
            name='recepteur',
        ),
        migrations.AddField(
            model_name='message',
            name='recepteurs',
            field=models.ManyToManyField(related_name='recepteur_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='emetteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emetteur_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='documents',
            field=models.ManyToManyField(to='gestioncouriers.document'),
        ),
    ]
