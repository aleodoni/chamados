# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0011_auto_20150909_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='executor',
            field=models.ForeignKey(to='telefonia.Executor', blank=True),
        ),
    ]
