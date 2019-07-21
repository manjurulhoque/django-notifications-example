from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.template.defaultfilters import slugify

from .models import *
from .forms import UserLoginForm


# Create your views here.
def index(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 5)
    page = request.GET.get('page', 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'posts/index.html', {'posts': posts})


def create_post(request):
    if request.method == "POST":
        title = request.POST['title']
        text = request.POST['text']
        cat = Category.objects.get(id=int(request.POST['category_id']))
        photo = request.FILES['image']
        # return HttpResponse(cat)
        post = Post(title=title, text=text, photo=photo)
        post.save()
        if post.categories.add(cat):
            return redirect('/')
    categories = Category.objects.all()
    return render(request, 'posts/create.html', {'categories': categories})


def show_post(request, id):
    if request.method == "POST":
        text = request.POST['text']
        post = Post.objects.get(id=id)
        comment = Comment(text=text, post=post)
        if comment.save():
            post = Post.objects.get(id=id)
            return render(request, 'posts/show.html', {'post': post})
    post = Post.objects.get(id=id)
    return render(request, 'posts/show.html', {'post': post})


def category(request):
    categories = Category.objects.all()
    return render(request, 'categories/index.html', {'categories': categories})


def create_category(request):
    if request.method == "POST":
        name = request.POST['name']

        Category(name=slugify(name)).save()
        return redirect('/categories')
    return render(request, 'categories/create.html', {})


def show_category_post(request, name):
    cat = Category.objects.get(name=name)
    posts = cat.post_set.all()
    return render(request, 'posts/category_posts.html', {'posts': posts})


def edit_category(request, id=None):
    cat = Category.objects.get(id=id)
    return render(request, 'categories/edit.html', {'category': cat})


def update_category(request, id=None):
    cat = Category.objects.get(id=id)
    cat.name = request.POST['name']
    cat.save()
    return redirect('/categories')


def delete_category(request, id=None):
    cat = Category.objects.get(id=id)
    if cat.delete():
        return redirect('/categories')
    return redirect('/categories')


def signup(request):
    return render(request, '')


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
    return render(request, 'form.html', {'form': form, "title": title})
