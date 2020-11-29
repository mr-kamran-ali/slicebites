# Generated by Django 3.1.3 on 2020-11-23 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=24)),
                ('base_price', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pizzeria.size')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
                ('is_made', models.BooleanField(default=False)),
                ('is_collected', models.BooleanField(default=False)),
                ('is_delivered', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzeria.customer')),
                ('pizzas', models.ManyToManyField(blank=True, to='pizzeria.Pizza')),
            ],
        ),
    ]
