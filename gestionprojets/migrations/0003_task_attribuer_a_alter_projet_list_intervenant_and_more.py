# Generated by Django 4.1.4 on 2022-12-11 00:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("gestionprojets", "0002_client_projet_budget_projet_chef_project_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="attribuer_a",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attribuer_a",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="projet",
            name="list_intervenant",
            field=models.ManyToManyField(
                related_name="intervenant", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="list_intervenant",
            field=models.ManyToManyField(
                related_name="intervenant_task", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
