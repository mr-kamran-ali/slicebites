# Generated by Django 3.1.3 on 2020-11-27 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0010_auto_20201124_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(default=191, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pizzeria.order'),
            preserve_default=False,
        ),
    ]
