# -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.models.fields import PageField

from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.folder import FilerFolderField
from filer.fields.image import FilerImageField

from .utils import get_additional_styles


class GalleryPlugin(CMSPlugin):
    STANDARD = 'standard'
    FEATURE = 'feature'

    STYLE_CHOICES = [
        (STANDARD, _('Standard')),
        (FEATURE, _('Feature'))
    ]

    ENGINE_CHOICES = (
        ('fade', _('Fade')),
        ('slide', _('Slide'))
    )

    style = models.CharField(
        _('Style'), choices=STYLE_CHOICES + get_additional_styles(), default=STANDARD, max_length=50)
    engine = models.CharField(_('Engine'), choices=ENGINE_CHOICES, default=ENGINE_CHOICES[0][0], max_length=50)
    timeout = models.IntegerField(_('Timeout'), default=5000, help_text=_("Set to 0 to disable autoplay"))
    duration = models.IntegerField(_('Duration'), default=300)
    shuffle = models.BooleanField(_('Shuffle slides'), default=False)

    def __unicode__(self):
        style = _('Style')
        engine = _('Engine')
        timeout = _('Timeout')
        duration = _('Duration')
        shuffle = _('Shuffle Slides')
        return u'%s: %s, %s: %s, %s: %i, %s: %i, %s: %s' % (
            style, self.style.title(), engine, self.engine.title(),
            timeout, self.timeout, duration, self.duration, shuffle, self.shuffle
        )


class SlidePlugin(CMSPlugin):
    LINK_TARGETS = (
        ('', _('same window')),
        ('_blank', _('new window')),
        ('_parent', _('parent window')),
        ('_top', _('topmost frame')),
    )

    image = FilerImageField(verbose_name=_('image'), blank=True, null=True)
    content = HTMLField("Content", blank=True, null=True)
    url = models.URLField(_("Link"), blank=True, null=True)
    page_link = PageField(
        verbose_name=_('Page'),
        blank=True,
        null=True,
        help_text=_("A link to a page has priority over a text link.")
    )
    target = models.CharField(
        verbose_name=_("target"),
        max_length=100,
        blank=True,
        choices=LINK_TARGETS,
    )


    def __unicode__(self):
        image_text = content_text = None

        if self.image_id:
            image_text = u'%s' % (self.image.name or self.image.original_filename)
        if self.content:
            text = strip_tags(self.content).strip()
            if len(text) > 100:
                content_text = u'%s...' % text[:100]
            else:
                content_text = u'%s' % text

        if image_text and content_text:
            return u'%s (%s)' % (image_text, content_text)
        else:
            return image_text or content_text

    def get_link(self):
        if self.page_link_id:
            return self.page_link.get_absolute_url()
        if self.url:
            return self.url
        return False


class SlideFolderPlugin(CMSPlugin):
    folder = FilerFolderField(verbose_name=_('folder'))
