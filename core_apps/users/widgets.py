from django.forms import widgets
from django.template.loader import render_to_string
from django import forms


class CloudinaryOrLocalFileWidget(widgets.FileInput):
    template_name = 'admin/widgets/cloudinary_file_widget.html'

    class Media:
        css = {
            'all': ('admin/css/cloudinary_widget.css',)
        }
        js = ('admin/js/cloudinary_widget.js',)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}

        if value and hasattr(value, 'url'):
            value_dict = {'url': value.url, 'name': str(value)}
        else:
            value_dict = None

        context = {
            'widget': {
                'name': name,
                'value': value_dict,
                'attrs': attrs,
            }
        }
        return render_to_string(self.template_name, context)
