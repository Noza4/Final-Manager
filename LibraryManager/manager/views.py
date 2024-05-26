from datetime import date
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.views import APIView
from manager.forms import LoginForm, CustomUserCreationForm, ReservationForm, BookReservationForm
from manager.models import BookReservation, CustomUser
from rest_framework import generics
from manager.serializers import BookSerializer, BookReservationSerializer, CustomUserSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Book, Author, Genre


def home(request):
    query = request.GET.get('query')
    author_id = request.GET.get('author')
    genre_id = request.GET.get('genre')

    books = Book.objects.all().order_by('title')

    if query:
        books = books.filter(title__icontains=query)

    if author_id:
        books = books.filter(author__id=author_id)

    if genre_id:
        books = books.filter(genre__id=genre_id)

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    authors = Author.objects.all()
    genres = Genre.objects.all()

    context = {
        'page_obj': page_obj,
        'authors': authors,
        'genres': genres,
    }

    return render(request, "home.html", context=context)


def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        print(book.author)
        return render(request, 'info.html', context={'book': book})

    except Book.DoesNotExist:
        return JsonResponse({'ERROR': 'THE BOOK WITH THIS ID IS NOT AVAILABLE'}, status=404)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['email'] = form.cleaned_data.get('email')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    email = request.session.pop('email', '')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_user:
                    return redirect('home')
                elif user.is_staff:
                    return redirect('home')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm(initial={'email': email})

    return render(request, 'login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def crud(request):
    return render(request, "crud.html")


def book_list(request):
    query = request.GET.get('q')
    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query)

    return render(request, 'book_list.html', {'books': books})


@login_required
def reserve(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            book.stock -= 1
            reservation = form.save(commit=False)
            reservation.book = book
            reservation.email = request.user.email
            reservation.save()
            # Add success message
            return HttpResponse("<h1 style='text-align: center; margin-top: 250px;'>Book Is Reserved !</h1>")
    else:
        form = ReservationForm(initial={'book': book_id, 'email': request.user.email})

    return render(request, 'reservation.html', {'form': form})


class Top10(generics.ListAPIView):
    queryset = Book.objects.all().order_by("popularity")[:10]
    serializer_class = BookSerializer


class UpdateBook(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_field = "pk"


class AddBook(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def remove_reservation(request):
    if request.method == 'POST':
        reservation_id = request.POST.get('reservation_id')
        try:

            reservation = BookReservation.objects.get(id=reservation_id, status='Reserved')


            reservation.status = 'Cancelled'
            reservation.save()


            book = reservation.book
            book.stock = F('stock') + 1
            book.save()

            return JsonResponse({'success': True, 'message': 'Reservation removed successfully.'})
        except BookReservation.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Reservation does not exist or is not reserved.'},
                                status=404)
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


def admin_dash(request):
    data = BookReservation.objects.all()
    return render(request, "admin_dash.html", {"data": data})


def return_book(request, reservation_id):
    reservation = get_object_or_404(BookReservation, id=reservation_id)

    if request.method == 'POST':
        actual_return_date = date.today()
        expected_return_date = reservation.return_date

        if actual_return_date > expected_return_date:
            reservation.status = 'Late'
        else:
            reservation.status = 'Returned'

        reservation.save()


        book = reservation.book
        book.stock += 1
        book.save()

        return redirect('admin_dash')

    return render(request, 'return_book.html', {'reservation': reservation})


def take_out_book(request):
    if request.method == 'POST':
        form = BookReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()


            book = reservation.book
            book.stock = F('stock') - 1
            book.popularity = F('popularity') + 1
            book.save()

            return redirect('admin_dash')
    else:

        initial_data = {'reserve_date': date.today()}
        form = BookReservationForm(initial=initial_data)

    return render(request, 'take_out.html', {'form': form})


class TopLateBooksAPIView(APIView):
    def get(self, request):

        books_with_late_count = BookReservation.objects.filter(status="Late").values('book').annotate(
            late_count=Count('id')).order_by('-late_count')[:100]

        book_ids = [item['book'] for item in books_with_late_count]
        top_late_reservations = BookReservation.objects.filter(book__in=book_ids, status="Late")

        serializer = BookReservationSerializer(top_late_reservations, many=True)
        return Response(serializer.data)


class TopLateUsersAPIView(APIView):
    def get(self, request):

        users_with_late_count = BookReservation.objects.filter(status="Late").values('name_id').annotate(late_count=Count('id')).order_by('-late_count')[:100]


        user_ids = [item['name_id'] for item in users_with_late_count]
        top_late_users = CustomUser.objects.filter(id__in=user_ids)


        serializer = CustomUserSerializer(top_late_users, many=True)
        return Response(serializer.data)