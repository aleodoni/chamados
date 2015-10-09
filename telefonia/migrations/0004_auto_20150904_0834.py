# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0003_delete_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chamado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('abertura', models.DateField()),
                ('fechamento', models.DateField()),
                ('solicitante', models.CharField(max_length=300)),
                ('problema', models.CharField(max_length=500)),
                ('execucao', models.CharField(max_length=300)),
                ('departamento', models.ForeignKey(to='telefonia.Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Executor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='chamado',
            name='executor',
            field=models.ForeignKey(to='telefonia.Executor'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='ramal_atendimento',
            field=models.OneToOneField(related_name='ramal_atendimento', to='telefonia.Ramal'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='ramal_contato',
            field=models.OneToOneField(related_name='ramal_contato', to='telefonia.Ramal'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='status',
            field=models.ForeignKey(to='telefonia.Status'),
        ),
        migrations.AddField(
            model_name='chamado',
            name='urgencia',
            field=models.ForeignKey(to='telefonia.Urgencia'),
        ),
    ]
