# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0012_auto_20151105_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='executor',
            field=models.ForeignKey(blank=True, to='telefonia.Executor', null=True),
        ),
    ]
