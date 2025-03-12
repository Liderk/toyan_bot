from django.utils.html import format_html


def get_full_image_link(url):
    preview = format_html(f'<img src="{url}" style="max-height: 200px;">')
    return format_html(f'<a href="{url}" target="_blank">{preview}</a>')
