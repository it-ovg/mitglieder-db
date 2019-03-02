import os
from django import template
from django.conf import settings
from random import randint
import re

register = template.Library()


from random import randint

@register.filter('klass')
def klass(field):
    return field.field.__class__.__name__


@register.filter(name='has_group')
def has_group(user, group_name):
    from django.contrib.auth.models import Group
    group =  Group.objects.get(name=group_name)
    if group in user.groups.all():
        return group
    elif user.is_superuser:
        return group

    #return group in user.groups.all()

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class":css})


@register.filter(name='tex_safe')
def tex_safe(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless ',
        '>': r'\textgreater ',
    }
    regex = re.compile('|'.join(re.escape(key) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)
