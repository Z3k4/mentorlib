from django import template
import locale
from pathlib import Path
from mentorlib.settings import BASE_DIR

register = template.Library()

@register.filter
def format_date_to_local(date,local='fr_FR'):
    locale.setlocale(locale.LC_TIME, local)
    return date.strftime("%A %d %b %H:%M").capitalize()

@register.filter
def verbose_name(object) -> str:
    return object.__class__.__name__

@register.filter
def get_filter_template(filter):
    template_dir = Path(f"partials/core/filters/")
    template_path = template_dir / f"{verbose_name(filter).lower()}.html"
    full_path = BASE_DIR / "templates" / template_path

    if full_path.exists():
        return str(template_path)
    else:
        return str(template_dir / "default.html")
    
@register.filter
def get_attr(value, attr):
    return value.getlist(attr, [])