# Generated by Django 3.2.5 on 2022-10-17 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0008_alter_subject_online_source'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='date_of_birth',
            new_name='data_of_test',
        ),
    ]