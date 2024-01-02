from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import CreateUserForm, LoginUserForm, CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
# - Authentication models/funcs
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def like_view(request, pk):
    post = get_object_or_404(Article, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog:article-detail', args=[str(pk)]))


@login_required(login_url="blog:login")
def articles_list_view(request):
    queryset = Article.objects.all().order_by('-created_on')
    context = {
        "object_list": queryset
    }
    return render(request, "articles/article_list.html", context)


@login_required(login_url="blog:login")
def article_detail_view(request, pk):
    obj = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(article=obj)
    form = CommentForm()
    total_likes = obj.total_likes()
    liked = False
    if obj.likes.filter(id=request.user.id).exists():
        liked = True

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=request.user,
                content=form.cleaned_data["body"],
                article=obj,
            )
            comment.save()
            return HttpResponseRedirect(request.path_info)

    context = {
        "obj": obj,
        "comments": comments,
        "form": form,
        "total_likes": total_likes,
        "liked": liked,
    }
    return render(request, "articles/article_detail.html", context)


def RegisterPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('blog:login'))
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    form = LoginUserForm()

    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)

                return redirect('blog:article-list')

    context = {
        'loginform': form
    }

    return render(request, 'accounts/login.html', context=context)


def logout_page(request):
    logout(request)
    return redirect('blog:article-list')