from __future__ import unicode_literals

import json

from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class IoniconsInput(forms.TextInput):

    template = 'ionicons-input.html'

    class Media:
        js = (
            'bower_components/jquery/dist/jquery.min.js',
            'bower_components/bootstrap/dist/js/bootstrap.min.js',
            'bower_components/jquery.scrollTo/jquery.scrollTo.min.js',
            'appdata/js/ionicons_input.js',

        )
        css = {
            'all': (
                'bower_components/bootstrap/dist/css/bootstrap.min.css',
                'bower_components/Ionicons/css/ionicons.css',
                'css/main.css'
            )
        }

    def get_icons(self):
        from django.conf import settings
        import os
        filepath = os.path.join(settings.BASE_DIR, 'ionicons.json')
        with open(filepath, 'r') as json_file:
            data = json.load(json_file)
            return data.get('classes')
        return []

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'form-control vTextField'
        context = {
            'input': super(IoniconsInput, self).render(name, value, attrs),
            'name': name,
            'icons': self.get_icons()
        }

        return mark_safe(render_to_string(self.template, context=context))