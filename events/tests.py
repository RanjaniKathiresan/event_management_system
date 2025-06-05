from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from events.models import Events, Attendee
from django.contrib.auth import get_user_model
import pytz

User = get_user_model()

class ViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.event = Events.objects.create(
            event_name='Test Event',
            location='Test Location',
            start_time=timezone.now() + timezone.timedelta(days=1),
            end_time=timezone.now() + timezone.timedelta(days=2),
            max_capacity=2,
            is_active=True
        )
        self.attendee_data = {
            'attentee_name': 'John Doe',
            'email_id': 'john@example.com'
        }

    def test_register_view(self):
        url = reverse('register')
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpass123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)

    def test_login_view(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_event_create_and_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('create_retrive_events')
        event_data = {
            'event_name': 'Another Event',
            'location': 'Another Location',
            'start_time': (timezone.now() + timezone.timedelta(days=3)).astimezone(pytz.timezone('Asia/Kolkata')).isoformat(),
            'end_time': (timezone.now() + timezone.timedelta(days=4)).astimezone(pytz.timezone('Asia/Kolkata')).isoformat(),
            'max_capacity': 10,
            'is_active': True
        }
        response = self.client.post(url, event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_register_attendee(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('register_attendee', args=[self.event.id])
        response = self.client.post(url, self.attendee_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])

    def test_retrieve_attendees(self):
        self.client.force_authenticate(user=self.user)
        Attendee.objects.create(event=self.event, attentee_name='Jane Doe', email_id='jane@example.com')
        url = reverse('retrieve_attendees', args=[self.event.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list) or 'results' in response.data)

    def test_logout_view(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successfully logged out.')
