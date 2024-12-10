from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.http import HttpResponseRedirect
from .forms import PostForm
from django.contrib.auth.decorators import login_required  # If using authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def blog_list(request):
    post = Post.objects.all()
    context = {

        'blog_list':post
    }
    return render(request, "blog/blog_list.html",context)

# Create you@login_required  # If using authentication
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user has already liked the post (optional)
    if request.user in post.liked_by.all():
        post.liked_by.remove(request.user)
        post.likes -= 1
    else:
        post.liked_by.add(request.user)
        post.likes += 1
    
    post.save()
    return redirect('blog_detail', post_id=post.id)  # Redirect back to the post detailr views here.


def blog_detail(request, post_id):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to view this blog post.")
        return redirect('login')  # Redirect to login page if not logged in

    each_post = get_object_or_404(Post, id=post_id)
    context = {
        'blog_detail': each_post
    }
    return render(request, "blog/blog_detail.html", context)

def blog_delete(request,id):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to delete this blog post.")
        return redirect('login')  # Redirect to login page if not logged in

    each_post = Post.objects.get(id = id)
    each_post.delete()
    return HttpResponseRedirect('/posts/')

def blog_update(request,id):
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to update this blog post.")
        return redirect('login')  # Redirect to login page if not logged in
    post = Post.objects.get(id=id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/posts/')
    context = {
        "form": form,
        'form_type':'Update'
    }
    return render(request,"blog/blog_create.html",context)

def blog_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/posts/')
    context = {
        "form": form,
        'form_type':'Create'
    }
    return render(request,"blog/blog_create.html",context)
    
def user_login(request):
    """
    Renders the login page and handles user login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('blog_list')  # Redirect to the blog list page
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'blog/login.html')  # Render login page with the layout

def user_signup(request):
    """
    Renders the signup page and handles user registration.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect('login')  # Redirect to login page

    return render(request, 'blog/signup.html')  # Render signup page with the layout

def user_logout(request):
    """
    Logs out the user and redirects to the home page with a success message.
    """
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('blog_list')  # Redirect to the blog list or any other desired page



    # views.py
from rest_framework.viewsets import ModelViewSet
from .models import Post
from .serializers import PostSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
