from django import template
from django.contrib.auth.models import Group 
from django.shortcuts import get_object_or_404
register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  get_object_or_404(Group, name=group_name)
    return group in user.groups.all() 

@register.filter(name='has_bloc_navigation') 
def has_bloc_navigation(user, bloc):
    return user.has_bloc_navigation(bloc)

@register.filter(name='has_object') 
def has_object(user, model_name):
    return user.has_object(model_name)