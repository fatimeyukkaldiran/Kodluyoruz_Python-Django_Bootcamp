from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


STATUS = [
    ('draft', 'Taslak'),
    ('published', 'Yayinlandi'),
    ('deleted', 'Silindi'),
]

DEFAULT_STATUS = "draft"

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(
        max_length=200, 
        blank=True, 
        unique=True,
    )
    viewed = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default=DEFAULT_STATUS,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def user_viewed(self):
        self.viewed += 1
        self.save()
        return f"{self.viewed}"

    def get_absolute_url(self):
        # return f"/category/{self.slug}/"
        # /category/self.slug/
        return reverse(
            'cat', 
            kwargs={'cat_slug':self.slug }
        )

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(
        max_length=200, 
        blank=True, 
        unique=True,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default=DEFAULT_STATUS,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
    )
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(
        max_length=200, 
        blank=True, 
        unique=True,
    )
    content = models.TextField(null=True)
    cover_image = models.ImageField(upload_to='post', blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default=DEFAULT_STATUS,
    )
    viewed = models.PositiveIntegerField(default=0)
    total_loved =  models.PositiveIntegerField(default=0)
    is_home = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_total_loved(self):
        self.total_loved = self.postlove_set.filter(is_love=True).count()
        self.save()


    def user_viewed(self):
        self.viewed += 1
        self.save()
        return f"{self.viewed}"

    def get_tags_in_a(self):
        return self.tags.filter(
            title__icontains='a'
        )
    
    def get_latest_posts(self):
        latest_posts = Post.objects.filter(
            category=self.category,
            status="published"
        ).exclude(id=self.id)[:5]
        return latest_posts
    
    def get_absolute_url(self):
        # return f"/category/{self.slug}/"
        # /category/self.slug/
        return reverse(
            'post_detail',  #urls.py
            kwargs={
                'cat_slug': self.category.slug,
                'post_slug': self.slug 
            }
        )

    def get_love_count(self):
        return self.postlove_set.filter(is_love=True).count()

    def get_not_love_count(self):
        return self.postlove_set.filter(is_love=False).count()

    def __str__(self):
        return self.title


class PostLove(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_love = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=PostLove)
def save_profile(sender, instance, **kwargs):
    print("Signa Calisti")
    print(instance)
    instance.post.check_total_loved()