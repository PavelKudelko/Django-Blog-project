from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Comment
from .forms import CreateUserForm, LoginUserForm, CommentForm, ArticleForm, EditProfileForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views import generic
from django.views.generic.edit import FormView
# - Authentication models/funcs
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

# Create your views here.


class ChangePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('blog:password-success')


def password_success(request):
    return render(request, 'accounts/password_success.html', {})


def user_edit_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # Process the form data here if needed
            form.save()
            return redirect(reverse('article-list'))
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'accounts/edit_profile.html', {'form': form})


# A lot of useless parts of code, need refactoring. works properly
@login_required(login_url="blog:login")
def edit_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if str(request.user) != str(article.author):
        messages.error(request, "You don't have permission to edit this article.")
        return redirect('blog:article-list')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully.")
            return redirect('blog:article-detail', pk=pk)
    else:
        form = ArticleForm(instance=article)

    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/edit_article.html', context)


# A lot of useless parts of code, need refactoring. works properly
@login_required(login_url="blog:login")
def delete_article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if str(request.user) != str(article.author):
        messages.error(request, "You don't have permission to delete this article.")
        return redirect('blog:article-list')

    if request.method == "POST":
        article.delete()
        messages.success(request, "Article deleted successfully.")
        return redirect('blog:article-list')

    context = {
        'article': article,
    }
    return render(request, 'articles/delete_article.html', context)


@login_required(login_url="blog:login")
def add_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.username
            article.save()
            return redirect('blog:article-list')
    else:
        form = ArticleForm()

    context = {
        "form": form,
    }
    return render(request, "articles/add_article.html", context)


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
def articles_category(request, category):
    queryset = Article.objects.filter(
        categories__name__contains=category
    ).order_by('-created_on')
    context = {
        "category": category,
        "object_list": queryset
    }
    return render(request, "articles/article_category.html", context)


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

    is_author = request.user.username == obj.author

    context = {
        "obj": obj,
        "comments": comments,
        "form": form,
        "total_likes": total_likes,
        "liked": liked,
        "is_author": is_author,
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