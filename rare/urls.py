"""
URL configuration for rare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rareapi.views import UserViewSet, PostView, CategoryViewSet, CommentView, TagView
from rest_framework.routers import DefaultRouter
from rareapi.views import CategoryViewSet, CommentView, TagView, UserViewSet, PostView, PostTagView
from django.conf.urls.static import static
from . import settings


router = DefaultRouter(trailing_slash=False)
router.register(r'posts', PostView, 'post')
router.register(r'categories', CategoryViewSet, 'category')
router.register(r"comments", CommentView, "comment")
router.register(r"tags", TagView, "tag")
router.register(r"post_tags", PostTagView, "post_tag")

urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
    path('login', UserViewSet.as_view({"post": "login_user"}), name="login"),
    path('register', UserViewSet.as_view({'post': 'register_account'}), name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
