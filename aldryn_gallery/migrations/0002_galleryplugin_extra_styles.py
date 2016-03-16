# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='galleryplugin',
            name='extra_styles',
            field=models.CharField(help_text='An arbitrary string of CSS classes to add', max_length=50, verbose_name='Extra styles', blank=True),
            preserve_default=True,
        ),
    ]
