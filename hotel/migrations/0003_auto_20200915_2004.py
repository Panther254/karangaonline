# Generated by Django 3.1.1 on 2020-09-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_food_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='image',
            field=models.ImageField(blank=True, default='hotelpic.jpg', null=True, upload_to='food_pics'),
        ),
    ]
