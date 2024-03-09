from celery import shared_task
import faker
from django.utils import timezone
from datetime import timedelta
import random
from .models import User, Profile
from django.db.models import F


fake = faker.Faker()


@shared_task(bind=True)
def populate_users_profiles(self):
    user_records = [
        User(email=fake.unique.email(), password=fake.password()) for _ in range(50000)
    ]
    User.objects.bulk_create(user_records)
    profile_records = [
        Profile(
            user= usr,
            subscription_start_date=timezone.now()
            - timedelta(minutes=random.randrange(0, 10)),
            subscription_end_date=timezone.now()
            + timedelta(minutes=random.randrange(0, 10)),
        )
        for usr in User.objects.all()
    ]

    Profile.objects.bulk_create(profile_records)
    return "User profiles populated successfully"


@shared_task(bind=True)
def update_subscription_time(self):
    
    profiles = Profile.objects.filter(subscription_end_date__gt=timezone.now())
    profiles.update(
        subscription_start_date=timezone.now(),
        subscription_end_date= timezone.now() + timedelta(minutes=10),
    )
