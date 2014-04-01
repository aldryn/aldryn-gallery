# -*- coding: utf-8 -*-
from aldryn_gallery.forms import GalleryPluginForm
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import GalleryPlugin, SlidePlugin


# Base Classes
class GalleryBase(CMSPluginBase):
    class Meta:
        abstract = True

    module = _('Gallery')


class GalleryChildBase(GalleryBase):
    class Meta:
        abstract = True

    render_template = False
    require_parent = True
    parent_classes = ['GalleryCMSPlugin']

    def render(self, context, instance, placeholder):
        # get style from parent plugin, render chosen template
        self.render_template = 'aldryn_gallery/plugins/%s/slide.html' % getattr(
            instance.parent.get_plugin_instance()[0], 'style',  GalleryPlugin.STANDARD)
        context['instance'] = instance
        return context


# Plugins
class GalleryCMSPlugin(GalleryBase):
    render_template = False
    name = _('Gallery')
    model = GalleryPlugin
    form = GalleryPluginForm
    allow_children = True
    child_classes = ['SlideCMSPlugin']

    def render(self, context, instance, placeholder):
        self.render_template = 'aldryn_gallery/plugins/%s/gallery.html' % instance.style
        context['instance'] = instance
        return context

plugin_pool.register_plugin(GalleryCMSPlugin)


class SlideCMSPlugin(GalleryChildBase):
    name = _('Slide')
    model = SlidePlugin

plugin_pool.register_plugin(SlideCMSPlugin)


