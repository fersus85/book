# Generated by Django 4.1.7 on 2023-04-05 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_book_owner_userbookrelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbookrelation',
            name='rate',
            field=models.PositiveIntegerField(choices=[(1, 'So so'), (1, 'Fine'), (1, 'Good'), (1, 'Amazing'), (1, 'Incredible')], default=None),
        ),
    ]
