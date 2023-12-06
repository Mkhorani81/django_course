from django import template
from ..models import Categoty
register = template.Library()

@register.simple_tag
def title():
    return "وبلاگ جنگو"

@register.inclusion_tag("blog/partials/categoryNavbar.html")
def categoryNavbar():
    return {
        "category" : Categoty.objects.filter(status=True)
    }