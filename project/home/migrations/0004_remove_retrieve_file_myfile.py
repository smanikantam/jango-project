# Generated by Django 4.1.4 on 2022-12-21 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_retrieve_file_myfile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retrieve_file',
            name='myfile',
        ),
    ]
