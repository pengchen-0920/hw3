# Generated by Django 4.0.3 on 2022-03-03 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('OrderId', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Customer', models.CharField(max_length=20)),
                ('Items', models.CharField(max_length=20)),
            ],
        ),
    ]