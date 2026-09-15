from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Sum

from .models import Event, Booking, UserProfile
from .serializers import EventSerializer, BookingSerializer
from .emails import send_welcome_email, send_booking_email

# ---------------- HELPER ----------------

def get_user_role(user):
    try:
        return user.profile.role
    except UserProfile.DoesNotExist:
        return 'user'


# ---------------- EVENTS ----------------

@api_view(['GET', 'POST'])
def events_api(request):

    # GET — ellaa events-um (public, for browsing)
    if request.method == 'GET':
        events = Event.objects.all().order_by('-id')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    # POST — organizer mattum create panna mudiyum
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(
                {"error": "Please login as organizer"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if get_user_role(request.user) != 'organizer':
            return Response(
                {"error": "Only organizers can create events"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)   # ← IMPORTANT
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- EVENT DETAILS ----------------

@api_view(['GET', 'PUT', 'DELETE'])
def event_detail_api(request, id):

    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    # GET — public
    if request.method == 'GET':
        return Response(EventSerializer(event).data)

    # PUT/DELETE — organizer + owner check
    if not request.user.is_authenticated:
        return Response(
            {"error": "Please login"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if get_user_role(request.user) != 'organizer':
        return Response(
            {"error": "Only organizers can modify events"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Owner check — idhu thaan multi-tenant
    if event.organizer != request.user:
        return Response(
            {"error": "You can only modify your own events"},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        event.delete()
        return Response(
            {"message": "Event deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


# ---------------- REGISTER ----------------
@api_view(['POST'])
def register_api(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'user')

    if not username or not email or not password:
        return Response(
            {"error": "All fields are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if role not in ['user', 'organizer']:
        return Response(
            {"error": "Invalid role"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Email already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # User create
    user = User.objects.create_user(username=username, email=email, password=password)

    # UserProfile explicit-a create pannunga (signal illa na)
    from .models import UserProfile   # ila already imported at top
    UserProfile.objects.get_or_create(user=user, defaults={'role': role})
    # if profile already exists with different role, update
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()

    try:
        send_welcome_email(user)
    except Exception as e:
        print(f">>> Welcome email error: {e}")
        # Email fail aana kooda register continue aaganum

    # Token create
    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "message": "Registration successful",
        "username": user.username,
        "email": user.email,
        "role": role,
        "token": token.key
    }, status=status.HTTP_201_CREATED)



# ---------------- LOGIN ----------------

@api_view(['POST'])
def login_api(request):

    username = request.data.get('username')
    password = request.data.get('password')
    expected_role = request.data.get('expected_role')

    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    role = get_user_role(user)

    if expected_role and role != expected_role:
        return Response(
            {"error": f"This is not a {expected_role} account"},
            status=status.HTTP_403_FORBIDDEN
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response({
        "message": "Login successful",
        "username": user.username,
        "email": user.email,
        "role": role,
        "token": token.key
    }, status=status.HTTP_200_OK)


# ---------------- BOOKING ----------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):

    event_id = request.data.get('event')
    tickets = int(request.data.get('tickets', 0))

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    if tickets <= 0:
        return Response(
            {"error": "Please select at least one ticket"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if event.seats < tickets:
        return Response(
            {"error": f"Only {event.seats} seats available"},
            status=status.HTTP_400_BAD_REQUEST
        )

    total_amount = event.price * tickets

    booking = Booking.objects.create(
        user=request.user,
        event=event,
        customer_name=request.user.username,
        customer_email=request.user.email,
        tickets=tickets,
        total_amount=total_amount
    )

    event.seats -= tickets
    event.save()
    send_booking_email(booking)
    return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


# ---------------- ORGANIZER DASHBOARD ----------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def organizer_dashboard(request):

    if get_user_role(request.user) != 'organizer':
        return Response(
            {"error": "Only organizers can access this"},
            status=status.HTTP_403_FORBIDDEN
        )

    # Only THIS organizer's events
    my_events = Event.objects.filter(organizer=request.user).order_by('-id')
    my_bookings = Booking.objects.filter(event__organizer=request.user)

    return Response({
        "total_events": my_events.count(),
        "total_bookings": my_bookings.count(),
        "total_customers": my_bookings.values('customer_email').distinct().count(),
        "total_income": my_bookings.aggregate(total=Sum('total_amount'))['total'] or 0,
        "events": EventSerializer(my_events, many=True).data,
    })


# ---------------- MY BOOKINGS (user) ----------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_bookings_api(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    return Response(BookingSerializer(bookings, many=True).data)