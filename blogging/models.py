from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.contrib.auth.models import User
from django.core import validators
from django.urls import reverse
from django.conf import settings

# Create your models here.
QUALIFICATION = [
    ('ug', 'UnderGraduate'),
    ('g', 'Graduate'),
    ('pg', 'PostGraduate')
]

class Categories(models.Model):
    name = models.CharField('Test', max_length=30, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("categories_detail", kwargs={"name": self.name})
    

class Post(models.Model):
    title = models.CharField(max_length=100, default='Post Title')
    description = models.TextField(validators=[validators.MinLengthValidator(50)])
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='images/', default=False)
    banner = models.ImageField(upload_to='images/', default=False)
    category_id = models.ManyToManyField(Categories)

    class Meta:
        ordering = ['-last_modified']

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,primary_key=True)
    profile_img = models.ImageField(upload_to='profile/', default=False)
    dob = models.DateField()
    qualification = models.CharField(max_length=15,choices=QUALIFICATION, default=None, blank=True)

def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.title, instance.slug)
        # self.slug = slugify(self.title)

pre_save.connect(slug_save, sender=Post)
