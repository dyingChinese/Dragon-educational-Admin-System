# Generated by Django 5.0.6 on 2024-06-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_alter_user_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='es_Oijl7iCz_20240606_5f3b615', max_length=40, unique=True),
        ),
    ]
