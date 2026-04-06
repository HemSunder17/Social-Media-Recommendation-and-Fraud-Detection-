from django.contrib.auth.models import AbstractUser
from django.db import models

INTEREST_CHOICES = [
    ('cars', 'Cars'),
    ('dogs', 'Dogs'),
    ('cats', 'Cats'),
    ('motivation', 'Motivation'),
    ('food', 'Food'),
    ('travel', 'Travel'),
    ('technology', 'Technology'),
    ('fitness', 'Fitness'),
    ('music', 'Music'),
    ('art', 'Art'),
]

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    interests = models.ManyToManyField('Interest', blank=True)
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Interest(models.Model):
    name = models.CharField(max_length=50, choices=INTEREST_CHOICES, unique=True)

    def __str__(self):
        return self.name