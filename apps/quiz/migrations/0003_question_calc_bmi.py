# Generated by Django 4.0.3 on 2022-03-31 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_remove_group_if_all_no_remove_group_if_any_yes'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='calc_bmi',
            field=models.BooleanField(default=False),
        ),
    ]