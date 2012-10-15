from django.template import Library
from django.conf import settings

register = Library()

@register.inclusion_tag('kiba/init_socials.html')
def init_socials(socials='vk,fb,google'):
    socials = socials.split(',')

    return {
        'socials': socials,

        'GOOGLE_CLIENT_ID': getattr(settings, 'GOOGLE_CLIENT_ID', ''),
        'GOOGLE_CLIENT_SECRET': getattr(settings, 'GOOGLE_CLIENT_SECRET',''),
        
        'VKONTAKTE_APP_ID': getattr(settings, 'VKONTAKTE_APP_ID',''),

        'FACEBOOK_APP_ID': getattr(settings, 'FACEBOOK_APP_ID',''),
    }