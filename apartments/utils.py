from django.contrib.admin.widgets import AdminFileWidget
from django.utils.html import format_html



          
class AdminImageWidget(AdminFileWidget):
    """Admin widget for showig clickable thumbnail of Image file fields"""

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value and getattr(value, 'url', None):
            html = format_html('<a href="{0}" target="_blank"><img src="{0}" alt="{1}" width="150" height="150" style="object-fit:cover;margin-bottom:30px; border:0.5px solid black;"/></a>', value.url, str(value)) + html
        return html 
     