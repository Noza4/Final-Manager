# Generated by Django 5.0.6 on 2024-05-26 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0019_alter_bookreservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreservation',
            name='status',
            field=models.CharField(choices=[('Reserved', 'Reserved'), ('On Loan', 'On Loan'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], max_length=50),
        ),
    ]
