# Generated by Django 4.0.3 on 2022-03-03 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Customer',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='Items',
            new_name='items',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='OrderId',
            new_name='optimizerderId',
        ),
    ]
