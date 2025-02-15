# Generated by Django 5.1.5 on 2025-02-05 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="username",
            field=models.CharField(
                default="default_username",
                help_text="Введите имя пользователя",
                max_length=150,
                unique=True,
                verbose_name="Имя пользователя",
            ),
        ),
    ]
