# Generated by Django 4.1.7 on 2023-04-05 08:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0005_remove_book_owner_alter_userbookrelation_rate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='readers',
            field=models.ManyToManyField(related_name='books', through='store.UserBookRelation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='book',
            name='owner',
        ),
        migrations.AddField(
            model_name='book',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_books', to=settings.AUTH_USER_MODEL),
        ),
    ]
