# Generated by Django 4.2.14 on 2024-08-07 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BoardManagement', '0002_rename_message_boradinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boradinfo',
            name='content',
            field=models.TextField(),
        ),
    ]
