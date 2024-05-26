from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from manager.models import BookReservation

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(label="Full Name")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'full_name', 'personal_number', 'birth_date')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class ReservationForm(forms.ModelForm):
    reserve_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = BookReservation
        fields = ['name', 'reserve_date']

    def __init__(self, *args, **kwargs):
        book_id = kwargs.pop('book_id', None)
        email = kwargs.pop('email', None)
        super().__init__(*args, **kwargs)
        if book_id:
            self.fields['book'].initial = book_id
        if email:
            self.fields['email'].initial = email

    def clean_reserve_date(self):
        reserve_date = self.cleaned_data['reserve_date']
        today = timezone.now().date()
        if reserve_date < today or reserve_date > today + timezone.timedelta(days=1):
            raise forms.ValidationError("Reservation date must be today or tomorrow.")
        return reserve_date


class BookReservationForm(forms.ModelForm):
    class Meta:
        model = BookReservation
        fields = ['name', 'book', 'email', 'reserve_date', 'status']
        widgets = {
            'reserve_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(choices=BookReservation.choice)
        }

