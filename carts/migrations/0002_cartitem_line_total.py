# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-14 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='line_total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
            preserve_default=False,
        ),
    ]
