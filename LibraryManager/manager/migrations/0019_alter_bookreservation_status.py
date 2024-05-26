# Generated by Django 5.0.6 on 2024-05-26 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0018_bookreservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreservation',
            name='status',
            field=models.CharField(choices=[('Reserved', 'Reserved'), ('On Loan', 'On Loan'), ('Cancelled', 'Cancelled')], max_length=50),
        ),
    ]
