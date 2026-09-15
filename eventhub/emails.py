from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    """User register aana udane welcome email anuppum"""
    subject = "Welcome to EventHub! 🎉"
    
    message = f"""
Hi {user.username},

Welcome to EventHub! 🎉

Your account has been created successfully.

You can now:
- Browse events
- Book tickets
- Get instant email confirmations

Login here: http://127.0.0.1:5173/login

Thanks for joining!
- Team EventHub
"""
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        print(f">>> Welcome email sent to {user.email}")
        return True
    except Exception as e:
        print(f">>> Welcome email FAILED: {e}")
        return False


def send_booking_email(booking):
    """Booking confirm aana udane email anuppum"""
    subject = f"Booking Confirmed - {booking.event.title}"
    
    message = f"""
Hi {booking.customer_name},

Your booking is confirmed! 🎉

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOOKING DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Booking ID: #{booking.id}
Event: {booking.event.title}
Date: {booking.event.date}
Time: {booking.event.time}
Location: {booking.event.location}

Tickets: {booking.tickets}
Total Amount: ₹{booking.total_amount}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Thank you for booking with EventHub!

See you at the event!
- Team EventHub
"""
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.customer_email],
            fail_silently=False,
        )
        print(f">>> Booking email sent to {booking.customer_email}")
        return True
    except Exception as e:
        print(f">>> Booking email FAILED: {e}")
        return False