# Generated by Django 5.0.6 on 2024-06-15 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('InstaBookApplication', '0006_rename_name_profile_firstname_profile_lastname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='firstName',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='lastName',
        ),
    ]
