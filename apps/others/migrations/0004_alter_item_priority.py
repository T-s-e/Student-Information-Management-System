# Generated by Django 3.2.5 on 2022-11-03 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('others', '0003_item_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='priority',
            field=models.CharField(choices=[('----', '----'), ('!', '较低'), ('!!', '一般'), ('!!!', '较高')], default='----', max_length=15),
        ),
    ]
