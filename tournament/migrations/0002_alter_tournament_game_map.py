# Generated by Django 4.2.16 on 2024-11-12 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tournament", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tournament",
            name="game_map",
            field=models.TextField(),
        ),
    ]