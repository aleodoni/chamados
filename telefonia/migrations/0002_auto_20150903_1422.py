# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nome', models.CharField(max_length=200)),
                ('login', models.CharField(max_length=20)),
                ('senha', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('consulta', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='problemas',
            options={'verbose_name_plural': 'problemas'},
        ),
        migrations.AlterModelOptions(
            name='ramal',
            options={'verbose_name_plural': 'ramais'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'status'},
        ),
    ]
