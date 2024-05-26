"""
URL configuration for LibraryManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include

from LibraryManager import settings
from manager.urls import url_path, api_url
from manager.views import home, book_detail, BookList, user_login, user_logout, reserve, \
    remove_reservation, admin_dash, take_out_book, return_book

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include(url_path), name="register"),
    path('', home, name="home"),
    path("item/", include(api_url)),
    path("book/<int:book_id>/", book_detail, name="get_book"),
    path("books", BookList.as_view()),
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout"),
    path("reservation/<int:book_id>", reserve, name="reservation"),
    path('remove_reservation/', remove_reservation, name='remove_reservation'),
    path('admin_dash', admin_dash, name="admin_dash"),
    path('take_out', take_out_book, name="book_take_out"),
    path('return/<int:reservation_id>', return_book, name="return_book"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
