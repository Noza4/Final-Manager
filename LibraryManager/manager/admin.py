from django.contrib import admin
from manager.models import Book, Author, Genre, CustomUser, BookReservation

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(CustomUser)

admin.site.index_title = "Library"
admin.site.site_header = "Library Manager"
admin.site.site_title = "Administration"


class BookManager(admin.ModelAdmin):
    search_fields = ('title', 'author__name', 'genre__name')
    list_filter = ('author', 'genre', 'publication_date', 'stock')
    list_display = ('title', 'stock',)
    filter_horizontal = ('author', 'genre')


admin.site.register(Book, BookManager)


class BookReservationManager(admin.ModelAdmin):

    search_fields = ("name",)

    list_filter = [
        "name", "status"
    ]

    list_display = [
        "name", "book", "email", "status", "id"
    ]


admin.site.register(BookReservation, BookReservationManager)


