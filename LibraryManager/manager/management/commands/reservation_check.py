from django.db.models import F
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from manager.models import BookReservation


class Command(BaseCommand):
    help = 'Checks reserved books and removes reservation if more than a day has passed since reservation date'

    def handle(self, *args, **kwargs):

        threshold_time = timezone.now().date() - timedelta(days=1)

        expired_reservations = BookReservation.objects.filter(status='Reserved', reserve_date__lt=threshold_time)

        for reservation in expired_reservations:
            reservation.status = 'Cancelled'
            reservation.book.stock = F('stock') + 1
            reservation.book.save()
            reservation.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully checked {expired_reservations.count()} reserved books'))

