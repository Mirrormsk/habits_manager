# Generated by Django 5.0 on 2024-01-03 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0005_alter_habit_related_habit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="reward",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="награда"
            ),
        ),
    ]