from django.urls import path
from manager.views import register, AddBook, UpdateBook, crud, Top10, TopLateBooksAPIView, TopLateUsersAPIView

url_path = [
    path("", register, name="register"),
]

api_url = [
    path("", crud, name="crud"),
    path("add", AddBook.as_view(), name="add"),
    path("update/<int:pk>/", UpdateBook.as_view(), name="update"),
    path("top", Top10.as_view(), name="top_10"),
    path('late', TopLateBooksAPIView.as_view(), name='top-late-books'),
    path('late-users', TopLateUsersAPIView.as_view(), name='top-late-users')

]
