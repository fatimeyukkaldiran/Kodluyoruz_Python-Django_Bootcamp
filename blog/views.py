from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import Http404, JsonResponse
from .models import Category, Post, PostLove, STATUS
from .forms import CategoryForm, CategoryModelForm, PostModelForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test

def user_is_admin(user):
    grp = Group.objects.get(name='BlogAdmin')
    return grp in user.groups.all()


@user_passes_test(user_is_admin)
def panel_list(request):
    return render(request, 'panel.html', {})


def index(request, cat_slug=None):
    context = dict()
    # context['categories'] = Category.objects.filter(
    #     status='published'
    # ).order_by('title')
    context['items'] = Post.objects.filter(
        status='published'
    ).order_by('-created_at')
    context['form'] = CategoryModelForm()
    if cat_slug:
        # category = Category.objects.get(slug=cat_slug)
        category = get_object_or_404(Category, slug=cat_slug)
        context['category'] = category
        category.user_viewed()
        context['items'] = context['items'].filter(
            category=category
        )
    
    return render(request, 'index.html', context)


# def category(request, cat_slug):
#     context = dict()
#     category = Category.objects.get(slug=cat_slug)
#     context['category'] = category
#     context['categories'] = Category.objects.filter(
#         status='published'
#     ).order_by('title')
#     context['items'] = Post.objects.filter(
#         category=category,
#         status='published'
#     ).order_by('-created_at')
#     return render(request, 'index.html', context)



def post_detail(request, cat_slug, post_slug):
    context = dict()
    item = get_object_or_404(Post, slug=post_slug)
    context['item'] = item
    item.user_viewed()
    # print(context['item'].category.user_viewed())
    # context['item'] = Post.objects.get(slug=post_slug)
    return render(request, 'blog/post.html', context)


def add_category(request):
    context = {
        'form': CategoryModelForm()
    }

    if request.method == "POST":
        if request.user.is_staff:
            form = CategoryModelForm(request.POST)
            title = form.data.get('title')
            try:
                item = Category.objects.create(
                    title = title, slug = title,
                    user=request.user,
                )
                messages.add_message(
                    request, messages.SUCCESS, f'{title} Saved'
                )
                if request.user.is_superuser:
                    item.status = "published"
                    item.save()
                    messages.add_message(
                        request, messages.SUCCESS, f'{title} Published'
                    )
                return redirect('panel')
            except Exception:
                print(Exception)
                messages.add_message(
                    request, messages.WARNING, 
                    f'{title} No Save'
                )

    return render(request, 'blog/add_category.html', context)


def add_post(request):
    form = PostModelForm()
    context = {'form': form}
    if request.method == "POST":
        form = PostModelForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
    return render(request, "blog/add_post.html", context)


def category_list(request):
    context = dict()
    grp = Group.objects.get(name='BlogAdmin')
    categories = Category.objects.all()
    context = {
        'categories_list': categories,
        # 'is_super': request.user.is_superuser,
        'is_admin': grp in request.user.groups.all()
    }
    return render(request, 'blog/categories.html', context)


def category_update_status(request, category_id, status):
    st = [item[0] for item in STATUS]
    if not status in st:
        return redirect('category_list')
    instance = Category.objects.get(id=category_id)
    instance.status = status
    instance.save()
    messages.add_message(request, messages.SUCCESS, 
        f"{instance.title} Deleted"
    )
    return redirect('category_list')


@login_required
def action_post_love(request, post_id):
    print(request.method)
    if request.method != 'POST' :
        return redirect('home')
    post = get_object_or_404(Post, id=post_id)
    try:
        post_love, created = PostLove.objects.get_or_create(
            user=request.user,
            post=post
        )
        if not created:
            post_love.is_love = not post_love.is_love
            post_love.save()
    except:
        post_loves = PostLove.objects.filter(
            user=request.user,
            post=post
        )
        post_loves = post_loves.exclude(pk=post_loves[0].pk)
        post_loves.delete()

        post_love, created = PostLove.objects.get_or_create(
            user=request.user,
            post=post
        )
        if not created:
            post_love.is_love = not post_love.is_love
            post_love.save()
    context = {
        'postLove': post_love.is_love,
        'postLoveCount': post_love.post.get_love_count()
    }
    return JsonResponse(context)
    # return redirect('home')