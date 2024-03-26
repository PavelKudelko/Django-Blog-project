from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (articles_list_view,
                    article_detail_view,
                    RegisterPage,
                    loginPage,
                    logout_page,
                    like_view,
                    articles_category,
                    add_article_view,
                    edit_article_view,
                    delete_article_view,
                    user_edit_view,
                    ChangePassword,
                    password_success,
                    # edit_profile_view,
                    )

app_name = 'blog'

urlpatterns = [
    path('', articles_list_view, name='article-list'),
    path('<int:pk>/', article_detail_view, name='article-detail'),
    path('register/', RegisterPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logout_page, name='logout'),
    # path('logout/', logout_page, name='logout'),
    path('like/<int:pk>', like_view, name='like-post'),
    path('category/<category>', articles_category, name='blog_category'),
    path('edit_profile/', user_edit_view, name='edit-profile'),
    path('new_article/', add_article_view, name='add-article'),
    path('<int:pk>/edit/', edit_article_view, name='edit-article'),
    path('<int:pk>/delete/', delete_article_view, name='delete-article'),
    # path('change_password/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html')),
    path('change_password/', ChangePassword.as_view(), name='change-password'),
    path('password_success/', password_success, name='password-success'),
    ]