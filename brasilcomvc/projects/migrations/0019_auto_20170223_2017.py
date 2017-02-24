# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_project_latlnt_not_editable'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectapply',
            options={'verbose_name': 'inscri\xe7\xe3o em projeto', 'verbose_name_plural': 'inscri\xe7\xf5es em projetos'},
        ),
    ]
