from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import PostModelForm, UserProfileForm, UserForm, LoginForm, UserUpdateForm
from .models import Post, UserProfile, Categories
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View

class PostList(ListView):
    model = Post
    template_name = 'blogging/home.html'
    paginate_by = 4
    context_object_name = 'posts'

class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostModelForm
    template_name = 'blogging/save_post.html'
    success_message = "Post created successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        res = super().form_valid(form)
        for obj in form.cleaned_data.get('category_id'):
            self.object.category_id.add(Categories.objects.get(id=obj.id))
        return res

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = 'blogging/update_post.html'
    context_object_name = 'post'


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blogging/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'


class PostDeleteView(DeleteView):
    model = Post
    slug_field = 'slug'
    success_url = reverse_lazy('index')

class UserLoginView(LoginView):
    template_name = 'blogging/user_login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

class CreateUserProfile(View):
    template_name = 'blogging/create_user.html'

    def get(self, request, *args, **kwargs):
        profile_form = UserProfileForm
        user_form = UserForm
        return render(request, self.template_name, {'form':user_form,'profile_form':profile_form})

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = user
            user_profile.save()
            authenticated_user = authenticate(username=user.username, password=password)
            login(request, authenticated_user)
            return HttpResponseRedirect('/')
        else:
            return render(request, self.template_name, {'form':user_form,'profile_form':profile_form})
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)


class UserDetailView(DetailView):
    model = User
    template_name = 'blogging/user_profile.html'
    context_object_name = 'user_p'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

class UserUpdateView(LoginRequiredMixin, View):
    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_userprofile(self, user):
        return get_object_or_404(UserProfile, user=user)

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        profile = self.get_userprofile(user)
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        return render(request, 'blogging/update_user.html',{'form':profile_form, 'user_form':user_form, 'user_p':user})

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        profile = self.get_userprofile(user)
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'blogging/user_profile.html',{'user_p':user})
        return render(request, 'blogging/update_user.html',{'form':profile_form, 'user_form':user_form, 'user_p':user})


def categories(request):
    categories = Categories.objects.all()
    return render(request, 'blogging/categories.html', {'categories':categories})

def category_detail(request,name):
    category = Categories.objects.get(name=name)
    if category:
        return render(request, 'blogging/category.html', {'category':category})

def category_post(request,id):
    post_objects = Categories.objects.get(pk=id).post_set.all()
    print(post_objects)
    page_objects = Paginator(post_objects, 4)
    page_no = request.GET.get('page')
    posts = page_objects.get_page(page_no)
    return render(request, 'blogging/home.html', {'posts':posts})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')