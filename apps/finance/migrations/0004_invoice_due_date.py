# Generated by Django 3.2.5 on 2022-11-05 08:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
