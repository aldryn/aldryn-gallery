# -*- coding: utf-8 -*-
from aldryn_gallery.forms import GalleryPluginForm
from django.utils.translation import ugettext_lazy as _
from django.conf.urls import patterns, url

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import GalleryPlugin, SlidePlugin


class GalleryBase(CMSPluginBase):
    module = 'Gallery'


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


class SlideCMSPlugin(GalleryBase):
    render_template = False
    name = _('Slide')
    model = SlidePlugin
    require_parent = True
    parent_classes = ['GalleryCMSPlugin']

    def render(self, context, instance, placeholder):
        # get style from parent plugin, render chosen template
        try:
            style = getattr(instance.parent.get_plugin_instance()[0], 'style')
        except AttributeError:
            style = GalleryPlugin.STANDARD

        self.render_template = 'aldryn_gallery/plugins/%s/slide.html' % style
        context['instance'] = instance
        return context

plugin_pool.register_plugin(SlideCMSPlugin)
