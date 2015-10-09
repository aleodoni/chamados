# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0004_auto_20150904_0834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='executor',
            options={'verbose_name_plural': 'executores'},
        ),
        migrations.AddField(
            model_name='executor',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='status',
            name='default',
            field=models.BooleanField(default=False),
        ),
    ]
