# Generated by Django 3.1.1 on 2020-10-20 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_auto_20201014_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='profile_pic.png', upload_to='customer_pics'),
        ),
    ]
