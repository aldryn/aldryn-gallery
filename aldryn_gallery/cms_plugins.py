# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .forms import GalleryPluginForm
from .models import GalleryPlugin, SlidePlugin, SlideFolderPlugin


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
        self.render_template = self.get_slide_template(instance)
        context['instance'] = instance
        context['image'] = instance.image
        return context

    def get_slide_template(self, instance):
        return 'aldryn_gallery/plugins/%s/slide.html' % getattr(
            instance.parent.get_plugin_instance()[0], 'style',  GalleryPlugin.STANDARD)


# Plugins
class GalleryCMSPlugin(GalleryBase):
    render_template = False
    name = _('Gallery')
    model = GalleryPlugin
    form = GalleryPluginForm
    allow_children = True
    child_classes = ['SlideCMSPlugin', 'SlideFolderCMSPlugin']

    def render(self, context, instance, placeholder):
        self.render_template = 'aldryn_gallery/plugins/%s/gallery.html' % instance.style
        context['instance'] = instance
        if instance.child_plugin_instances:
            number_of_slides = sum([plugin.folder.file_count if isinstance(plugin, SlideFolderPlugin) else 1
                                    for plugin in instance.child_plugin_instances])
        else:
            number_of_slides = 0
        context['slides'] = range(number_of_slides)
        return context


class SlideCMSPlugin(GalleryChildBase):
    name = _('Slide')
    model = SlidePlugin


class SlideFolderCMSPlugin(GalleryChildBase):
    name = _('Slide folder')
    model = SlideFolderPlugin
    render_template = 'aldryn_gallery/plugins/slide_folder.html'

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['slide_template'] = self.get_slide_template(instance)
        return context


plugin_pool.register_plugin(GalleryCMSPlugin)
plugin_pool.register_plugin(SlideCMSPlugin)
plugin_pool.register_plugin(SlideFolderCMSPlugin)
