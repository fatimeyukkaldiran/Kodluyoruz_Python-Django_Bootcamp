from django import template
from blog.models import PostLove

register = template.Library()

@register.simple_tag
def user_is_loved(request, post_id):
    is_loved = False
    if request.user.is_authenticated:
        is_loved = bool(
            PostLove.objects.filter(
                post_id=post_id, 
                user=request.user,
                is_love=True,
            )
        )
    return is_loved