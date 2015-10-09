# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0008_tipoequipamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamado',
            name='execucao',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='problema',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='ramal_atendimento',
            field=models.ForeignKey(related_name='ramal_atendimento', to='telefonia.Ramal'),
        ),
        migrations.AlterField(
            model_name='chamado',
            name='ramal_contato',
            field=models.ForeignKey(related_name='ramal_contato', to='telefonia.Ramal'),
        ),
    ]
