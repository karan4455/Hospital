# Generated by Django 4.0.5 on 2022-06-18 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
    ]
