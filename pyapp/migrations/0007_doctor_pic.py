# Generated by Django 4.0.5 on 2022-06-25 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyapp', '0006_rename_user_id_doctor_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='pic',
            field=models.FileField(default='media/default_doc.png', upload_to='media/images'),
        ),
    ]
