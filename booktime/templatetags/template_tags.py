from django import template
from booktime.models import ProductTag

register = template.Library()


@register.inclusion_tag('tags.html')
def get_tags_list(tag=None):
    return {'tags': ProductTag.objects.all(), 'act_tag': tag}