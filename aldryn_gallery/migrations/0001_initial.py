# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.folder
import djangocms_text_ckeditor.fields
import filer.fields.image
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('cms', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('style', models.CharField(default=b'standard', max_length=50, verbose_name='Style', choices=[(b'standard', 'Standard')])),
                ('engine', models.CharField(default=b'fade', max_length=50, verbose_name='Engine', choices=[(b'fade', 'Fade'), (b'slide', 'Slide')])),
                ('timeout', models.IntegerField(default=5000, help_text='Set to 0 to disable autoplay', verbose_name='Timeout')),
                ('duration', models.IntegerField(default=300, verbose_name='Duration')),
                ('shuffle', models.BooleanField(default=False, verbose_name='Shuffle slides')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='SlideFolderPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('folder', filer.fields.folder.FilerFolderField(verbose_name='folder', to='filer.Folder')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='SlidePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('content', djangocms_text_ckeditor.fields.HTMLField(null=True, verbose_name=b'Content', blank=True)),
                ('url', models.URLField(null=True, verbose_name='Link', blank=True)),
                ('target', models.CharField(blank=True, max_length=100, verbose_name='target', choices=[(b'', 'same window'), (b'_blank', 'new window'), (b'_parent', 'parent window'), (b'_top', 'topmost frame')])),
                ('link_anchor', models.CharField(max_length=128, verbose_name='link anchor', blank=True)),
                ('link_text', models.CharField(max_length=200, verbose_name='link text', blank=True)),
                ('image', filer.fields.image.FilerImageField(verbose_name='image', blank=True, to='filer.Image', null=True)),
                ('page_link', cms.models.fields.PageField(blank=True, to='cms.Page', help_text='A link to a page has priority over a text link.', null=True, verbose_name='Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
