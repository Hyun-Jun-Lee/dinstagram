# Generated by Django 3.0.14 on 2021-11-03 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0004_auto_20211103_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='message',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
