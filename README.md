This Django project, "Library Manager", serves as a management system for a library. It allows librarians to manage books, users, reservations, and other administrative tasks efficiently.

Features
Book Management: Add, update, and delete books. Each book includes details such as title, author(s), genre, publication date, stock, and image.
User Management: Admins can manage users, including librarians and regular users.
Reservation System: Users can reserve books, and librarians can manage these reservations, including marking books as reserved, on loan, returned, or late.
Dashboard: Provides a user-friendly interface for librarians to monitor book reservations, user activities, and other statistics.

Installation
Clone the repository:
git clone https://github.com/your_username/library-manager.git

Navigate to the project directory:
cd library-manager

Install dependencies:
pip install -r requirements.txt

Create a superuser (admin) account:
python manage.py createsuperuser

Run the development server:
python manage.py runserver

Access the admin panel at http://localhost:8000/admin/ and log in with the superuser credentials to manage the library.


Usage
Admin Dashboard: After logging in as a superuser, you can access the admin dashboard to manage books, users, reservations, and other administrative tasks.
Book Reservation: Regular users can log in and reserve books. Librarians can manage these reservations from the admin dashboard.
Book Management: Add, update, or delete books from the admin dashboard. Ensure to provide accurate details such as title, author(s), genre, publication date, and stock.
User Management: Admins can manage users, including librarians and regular users, from the admin dashboard.
Reservation System: Librarians can monitor and manage book reservations, mark books as reserved, on loan, returned, or late, from the admin dashboard.
