# Generated by Django 5.0.6 on 2024-05-26 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0015_bookreservation_email_alter_bookreservation_book'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookreservation',
            options={'verbose_name': 'Book Reservation'},
        ),
        migrations.AlterField(
            model_name='bookreservation',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
