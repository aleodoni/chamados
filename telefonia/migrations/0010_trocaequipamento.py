# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0009_auto_20150904_1435'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrocaEquipamento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serial', models.CharField(max_length=50)),
                ('motivo', models.CharField(max_length=500, null=True, blank=True)),
                ('chamado', models.ForeignKey(to='telefonia.Chamado')),
                ('tipo_equipamento', models.ForeignKey(to='telefonia.TipoEquipamento')),
            ],
        ),
    ]
