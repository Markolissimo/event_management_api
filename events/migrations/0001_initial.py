import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Initial migration for the events app.
    """

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date', models.DateTimeField(validators=[django.core.validators.MinValueValidator(django.utils.timezone.now)])),
                ('location', models.CharField(max_length=200)),
                ('capacity', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organized_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('refunded', 'Refunded')], default='pending', max_length=20)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='events.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-registration_date'],
            },
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['date'], name='events_even_date_5e8e1c_idx'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['location'], name='events_even_locatio_0ae1f4_idx'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['is_active'], name='events_even_is_acti_82811f_idx'),
        ),
        migrations.AddIndex(
            model_name='eventregistration',
            index=models.Index(fields=['status'], name='events_even_status_bdf692_idx'),
        ),
        migrations.AddIndex(
            model_name='eventregistration',
            index=models.Index(fields=['payment_status'], name='events_even_payment_6d05c3_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='eventregistration',
            unique_together={('event', 'user')},
        ),
    ]
