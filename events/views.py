from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from events.serializers import LoginSerializer, SignUpSerializer, EventSerializer, AttendeeSerializer
from events.models import Events
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone

# Create your views here.
class RegisterView(APIView):
    """View to handle user registration."""
    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=SignUpSerializer,
        responses={201: openapi.Response('User created', SignUpSerializer)}
    )
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Login and obtain authentication token",
        request_body=LoginSerializer,
        responses={200: openapi.Response('Login successful', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING)
        }))}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventView(APIView):
    """View to handle event creation."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new event (times in IST)",
        request_body=EventSerializer,
        responses={201: openapi.Response('Event created', EventSerializer)}
    )
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event created successfully", "event":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="List all upcoming events (times in IST)",
        responses={200: EventSerializer(many=True)}
    )
    def get(self, request):
        """List all upcoming (future) events."""
        now = timezone.now()
        events = Events.objects.filter(start_time__gt=now)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterAttendeeView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Register an attendee for an event",
        request_body=AttendeeSerializer,
        responses={201: openapi.Response('Registration successful', AttendeeSerializer)}
    )
    def post(self, request, event_id):
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=404)

        serializer = AttendeeSerializer(data=request.data, context={'event': event})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Registration successful!", "attendee": serializer.data}, status=201)
        return Response(serializer.errors, status=400)

class RetrieveAttendeeView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="List all attendees for an event (paginated)",
        responses={200: AttendeeSerializer(many=True)}
    )
    def get(self, request, event_id):
        try:
            event = Events.objects.get(id=event_id)
        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=404)

        attendees = event.attendees.all()
        serializer = AttendeeSerializer(attendees, many=True)
        return Response(serializer.data, status=200)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Log out the user by deleting their auth token",
        responses={200: openapi.Response('Successfully logged out', openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'message': openapi.Schema(type=openapi.TYPE_STRING)
        }))}
    )
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except AttributeError:
            pass
        except Exception:
            pass
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)