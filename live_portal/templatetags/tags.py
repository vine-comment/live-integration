from django import template
import logging
import base64

register = template.Library()

logger = logging.getLogger( __name__ )

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        logger.debug(pattern + request.path)
        return 'active'
    return ''
