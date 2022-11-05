# Generated by Django 3.2.5 on 2022-11-04 14:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corecode', '0004_auto_20201124_0614'),
        ('others', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('priority', models.CharField(choices=[('---------', '---------'), ('!', '较低'), ('!!', '一般'), ('!!!', '较高')], default='----', max_length=15)),
                ('date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('period', models.CharField(blank=True, max_length=200)),
                ('note', models.TextField(blank=True)),
                ('tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='corecode.tag')),
            ],
            options={
                'ordering': ['item', 'priority', 'tag'],
            },
        ),
    ]