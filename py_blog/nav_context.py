from blog.models import Category
from django.contrib.auth.models import Group
# py_blog/nav_context.py
# context_processor

def navbar(request):
    return {
        'categories': Category.objects.filter(
            status="published"
        )
    }


def user_is_admin_func(request):

    if  request.user.is_authenticated:
        user_is_admin=request.session.get('user_is_admin')
        if user_is_admin == None :
            grp = Group.objects.get_or_create(name='BlogAdmin')
            request.session['user_is_admin'] = grp[0] in request.user.groups.all()
    return {}        






