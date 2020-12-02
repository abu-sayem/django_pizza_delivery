# Generated by Django 3.0.7 on 2020-12-01 23:35

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('sm', 'small'), ('md', 'medium'), ('lg', 'large')], default='md', max_length=2)),
                ('count', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('status', models.CharField(choices=[('pe', 'pending'), ('de', 'delivered')], default='pe', max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Pizza')),
            ],
        ),
    ]