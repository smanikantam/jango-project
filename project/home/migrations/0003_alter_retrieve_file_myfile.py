# Generated by Django 4.1.4 on 2022-12-21 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_retrieve_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retrieve_file',
            name='myfile',
            field=models.FileField(max_length=1000, upload_to='MEDIA_ROOT/'),
        ),
    ]
