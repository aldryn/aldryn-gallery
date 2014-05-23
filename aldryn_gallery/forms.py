# -*- coding: utf-8 -*-
from django import forms
from django.template import TemplateDoesNotExist
from django.template.loader import select_template

from .models import GalleryPlugin


class GalleryPluginForm(forms.ModelForm):

    class Meta:
        fields = ['style', 'engine', 'timeout', 'duration', 'shuffle']
        model = GalleryPlugin

    def clean_style(self):
        style = self.cleaned_data.get('style')
        # Check if template for style exists:
        try:
            select_template(['aldryn_gallery/plugins/%s/gallery.html' % style])
        except TemplateDoesNotExist:
            raise forms.ValidationError("Not a valid style (Template does not exist)")
        return style
