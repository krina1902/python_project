# Generated by Django 4.2.3 on 2023-08-05 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_product_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='admin_access',
            field=models.BooleanField(default=False),
        ),
    ]
