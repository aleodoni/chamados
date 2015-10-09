# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0006_auto_20150904_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='fechamento',
            field=models.DateField(null=True, blank=True),
        ),
    ]
