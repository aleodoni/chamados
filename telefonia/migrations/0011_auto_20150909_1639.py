# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0010_trocaequipamento'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trocaequipamento',
            name='serial',
        ),
        migrations.AddField(
            model_name='trocaequipamento',
            name='serial_novo',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='trocaequipamento',
            name='serial_velho',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
