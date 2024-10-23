# Generated by Django 5.1.2 on 2024-10-23 17:38

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('rental_price', models.FloatField()),
                ('quantity', models.IntegerField()),
                ('condition', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=255)),
                ('country', models.CharField(max_length=255)),
                ('country_code', models.CharField(max_length=10)),
                ('image', models.ImageField(upload_to='uploads/items')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('favorited', models.ManyToManyField(blank=True, related_name='favorites', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Items',
            },
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('number_of_days', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('total_price', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rentals', to='item.item')),
            ],
            options={
                'verbose_name_plural': 'Rentals',
            },
        ),
    ]