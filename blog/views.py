from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.template.defaultfilters import slugify
from django.views.generic import FormView, CreateView
from notifications.models import Notification
from notifications.signals import notify

from .models import *
from .forms import *


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
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        print(request.FILES)
        title = request.POST['title']
        text = request.POST['text']
        cat = Category.objects.get(id=int(request.POST['category_id']))
        post = Post(title=title, text=text, category=cat, user=request.user)
        post.save()
        return redirect('/')
    categories = Category.objects.all()
    return render(request, 'posts/create.html', {'categories': categories})


def show_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        text = request.POST['text']
        comment = Comment(text=text, post=post)
        recipient = post.user
        if recipient != request.user:
            notify.send(request.user, recipient=recipient, verb='commented on your post',
                        level=Notification.LEVELS.success)
        if comment.save():
            return redirect('posts.show', {'id': post.id})
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
    title = "Register"
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password1")
        user.set_password(password)
        print(password)
        user.save()
        return redirect('login')
    return render(request, 'form.html', {'form': form, 'title': title})


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('posts')
    return render(request, 'form.html', {'form': form, "title": title})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("posts")
    return redirect("posts")

# class RegisterView(CreateView):
#     model = User
#     form_class = UserRegistrationForm
#     template_name = 'form.html'
#     success_url = '/'
#
#     extra_context = {
#         'title': 'Register'
#     }
#
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url())
#         return super().dispatch(self.request, *args, **kwargs)
#         # return super(Login, self).dispatch(request, *args, **kwargs)
#
#     def get_success_url(self):
#         return self.success_url
#
#     def post(self, request, *args, **kwargs):
#         # checking for email if is already taken or not
#         # username is by default unique
#         if User.objects.filter(email=request.POST['email']).exists():
#             return redirect('signup')
#
#         user_form = UserRegistrationForm(data=request.POST)
#
#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             print(user.password)
#             password = user_form.cleaned_data.get("password1")
#             user.set_password(password)
#             user.save()
#             return redirect('login')
#         else:
#             return render(request, 'form.html', {'form': user_form})
#
#
# class LoginView(FormView):
#     """
#         Provides the ability to login as a user with a username and password
#     """
#     success_url = '/'
#     form_class = UserLoginForm
#     template_name = 'form.html'
#
#     extra_context = {
#         'title': 'Login'
#     }
#
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             return HttpResponseRedirect(self.get_success_url())
#         return super().dispatch(self.request, *args, **kwargs)
#
#     def get_form_class(self):
#         return self.form_class
#
#     def form_valid(self, form):
#         login(self.request, form.get_user())
#         return HttpResponseRedirect(self.get_success_url())
#
#     def form_invalid(self, form):
#         """If the form is invalid, render the invalid form."""
#         return self.render_to_response(self.get_context_data(form=form))
