from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Post, Group, User
from .forms import PostForm

class PageBack:
    def __init__(self, request, _list):
        self.paginator = Paginator(_list, 10)
        self.page = self.paginator.get_page(request.GET.get('page'))

def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    page_back = PageBack(request, post_list)
    return render(request, 'index.html', {'page': page_back.page, 'paginator': page_back.paginator})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by("-pub_date")
    page_back = PageBack(request, post_list)
    return render(request, "group.html", {"group": group, 'page': page_back.page, 'paginator': page_back.paginator})

def group_all(request):
    group_list = Group.objects.all()
    page_back = PageBack(request, group_list)
    return render(request, "group_all.html", {'page': page_back.page, 'paginator': page_back.paginator})

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, "new_post.html", {"form": form})

def profile_view(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author).order_by("-pub_date")
    page_back = PageBack(request, post_list)
    return render(request, "profile.html", {"author": author, 'page': page_back.page, 'paginator': page_back.paginator})

def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id)
    if author != post.author:
        return render(request, "404.html")
    return render(request, "post.html", {"author": author, "post": post})

@login_required
def post_edit(request, username, post_id):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        return redirect('post', username=username, post_id=post_id)
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post', username=username, post_id=post_id)
    else:
        form = PostForm(instance=post)
    return render(request, "edit_post.html", {"form": form, "post": post})

def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)

def permission_denied(request, exception):
    return render(request, "misc/403.html", {"path": request.path}, status=403)

def server_error(request):
    return render(request, "misc/500.html", status=500)
