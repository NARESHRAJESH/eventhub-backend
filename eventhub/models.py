from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# ---------------- EVENT ----------------

class Event(models.Model):
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='events',
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seats = models.IntegerField()
    image = models.ImageField(upload_to='events/', null=True, blank=True)

    def __str__(self):
        return self.title


# ---------------- BOOKING ----------------

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    tickets = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.event.title}"


# ---------------- USER PROFILE ----------------

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('organizer', 'Organizer'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.user.username} - {self.role}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)