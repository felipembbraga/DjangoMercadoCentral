from django import forms
from django.contrib.admin.widgets import AdminFileWidget


class MCAdminImageWidget(AdminFileWidget):
    template_with_initial = (
        '<p class="file-upload">'
        '%(initial_text)s: <img src="%(initial_url)s"  height="80"/> '
        '%(clear_template)s<br />%(input_text)s: %(input)s'
        '</p>'
    )

