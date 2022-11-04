# Generated by Django 3.2.5 on 2022-11-04 14:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('corecode', '0004_auto_20201124_0614'),
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance_from_previous_term', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('active', 'Active'), ('closed', 'Closed')], default='active', max_length=20)),
                ('class_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='corecode.tag')),
            ],
            options={
                'ordering': ['item', 'term', 'subject'],
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_paid', models.IntegerField()),
                ('date_paid', models.DateField(default=django.utils.timezone.now)),
                ('comment', models.CharField(blank=True, max_length=200)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
                ('amount', models.IntegerField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.invoice')),
            ],
        ),
    ]
