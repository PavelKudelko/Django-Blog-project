from django.urls import path
from .views import articles_list_view, article_detail_view, RegisterPage, loginPage, logout_page, like_view

app_name = 'blog'

urlpatterns = [
    path('', articles_list_view, name='article-list'),
    path('<int:pk>/', article_detail_view, name='article-detail'),
    path('register/', RegisterPage, name='register'),
    path('login/', loginPage, name='login'),
    path('logout/', logout_page, name='logout'),
    # path('logout/', logout_page, name='logout'),
    path('like/<int:pk>', like_view, name='like-post'),
]