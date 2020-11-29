# Generated by Django 3.1.3 on 2020-11-24 13:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0009_auto_20201124_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='number',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='size',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='pizzeria.size'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='topping',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='toppings', to='pizzeria.topping'),
        ),
    ]
