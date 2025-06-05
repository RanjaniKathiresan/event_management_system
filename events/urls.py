from django.urls import path
from .views import RegisterView, LoginView, EventView, RegisterAttendeeView, RetrieveAttendeeView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('events/', EventView.as_view(), name='create_retrive_events'),
    path('events/<int:event_id>/register/', RegisterAttendeeView.as_view(), name='register_attendee'),
    path('events/<int:event_id>/attendees/', RetrieveAttendeeView.as_view(), name='retrieve_attendees'),
    path('logout/', LogoutView.as_view(), name='logout'),
]