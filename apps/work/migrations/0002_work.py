# Generated by Django 3.2.5 on 2022-11-04 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_method', models.CharField(choices=[('private', '个人'), ('collaboration', '协作')], default='private', max_length=15)),
                ('name', models.CharField(max_length=200)),
                ('period', models.CharField(default='None', max_length=200)),
                ('priority', models.CharField(choices=[('!', '较低'), ('!!', '一般'), ('!!!', '较高')], default='!', max_length=15)),
                ('note', models.TextField(blank=True)),
            ],
        ),
    ]
