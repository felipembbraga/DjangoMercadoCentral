from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from input_mask.contrib.localflavor.br.widgets import BRPhoneNumberInput
from django.conf import settings
from input_mask.utils import encode_options


class MCAdminImageWidget(AdminFileWidget):
    template_with_initial = (
        '<p class="file-upload">'
        '%(initial_text)s: <img src="%(initial_url)s"  height="80"/> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
        '</p>'
    )


class BRPhoneInput(forms.TextInput):

    class Media:
        js = (
            '%sbower_components/jquery/dist/jquery.min.js' % settings.STATIC_URL,
            '%sbower_components/jquery.maskedinput/dist/jquery.maskedinput.min.js' % settings.STATIC_URL,
            settings.STATIC_URL + 'misc/text_input_mask.js',
        )

    mask = {}

    def __init__(self, **kwargs):
        mask = kwargs.pop('mask', {})
        if type(mask) != object:
            mask = {'mask': mask}
        super(BRPhoneInput, self).__init__(**kwargs)

        self.mask.update(mask)

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['data-input-mask'] = encode_options(self.mask)
        return super(BRPhoneInput, self).render(name, value, attrs=attrs)
