# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telefonia', '0002_auto_20150903_1422'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
