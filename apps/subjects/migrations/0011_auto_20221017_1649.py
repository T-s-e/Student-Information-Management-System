# Generated by Django 3.2.5 on 2022-10-17 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0010_rename_data_of_test_subject_date_of_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='passport',
        ),
        migrations.AddField(
            model_name='subject',
            name='picture',
            field=models.ImageField(blank=True, upload_to='subjects/pictures/'),
        ),
    ]