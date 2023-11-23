import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from CDR.models import User, CDR, CallStatus, CallType
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.url_register = reverse('register')
        self.url_login = reverse('login')
        self.url_verify = reverse('verify')

        self.user1 = User.objects.create_user(email='test1@email.com', password='123')
        self.user2 = User.objects.create_user(email='test2@email.com', password='123')
        self.user3 = User.objects.create_user(email='test3@email.com', password='123')
        self.user1.confirmation_code = '1234'
        self.user1.confirmation_date = timezone.now() + timedelta(minutes=5)
        self.user1.save()

    @property
    def bearer_token(self):
        refresh = RefreshToken.for_user(self.user1)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def test_mock_register_user_and_get_sms_code(self):
        data = {
            "email": "2004.01027@manas.edu.kg",
            "password": "mock123abc!",
            "first_name": "mocked_name",
            "last_name": "mocked_last_name"
        }
        json_data = json.dumps(data)

        response = self.client.post(reverse('register'), data=json_data, content_type='application/json')
        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(201, response.status_code)

    def test_success_login_user(self):
        data = {
            'email': 'test1@email.com',
            'password': '123'
        }
        user = User.objects.get(email=data['email'])
        user.is_verified = True
        user.is_active = True
        user.save()
        json_data = json.dumps(data)
        response = self.client.post(reverse('login'), data=json_data, content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_user_verify(self):
        self.assertFalse(self.user1.is_verified)
        data = {
            "email": "test1@email.com",
            "code": "1234"
        }
        json_data = json.dumps(data)
        response = self.client.post(reverse('verify'), data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.is_verified)


class CDRAPITestCase(APITestCase):

    def setUp(self):

        self.user1 = User.objects.create_user(email='test3@email.com', password='123')
        self.user1.is_active = True
        self.user1.save()

        self.cdr1 = CDR.objects.create(calling_number='996704383070', called_number='996550605073',
                                       start_time='2023-11-20T16:55:59.646000+06:00', end_time='2023-11-21T16:55:59.646000+06:00',
                                       duration='00:15:00', call_status=CallStatus.successful, call_type=CallType.incoming)
        self.cdr2 = CDR.objects.create(calling_number='996704383070', called_number='996550605073',
                                       start_time='2023-11-22T16:55:59.646000+06:00', end_time='2023-11-23T16:55:59.646000+06:00',
                                       duration='00:15:00', call_status=CallStatus.rejected, call_type=CallType.missed)
        self.cdr3 = CDR.objects.create(calling_number='996704383070', called_number='996550605073',
                                       start_time='2023-11-22T16:55:59.646000+06:00', end_time='2023-11-23T16:55:59.646000+06:00',
                                       duration='00:15:00', call_status=CallStatus.unanswered, call_type=CallType.outgoing)
        self.cdr1.save()
        self.cdr2.save()
        self.cdr3.save()

    @property
    def bearer_token(self):
        refresh = RefreshToken.for_user(self.user1)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def test_cdr_detail(self):
        url = reverse('cdr-detail', kwargs={'pk': self.cdr1.pk})
        response = self.client.get(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cdr_that_doesnt_exists(self):
        url = reverse('cdr-detail', kwargs={'pk': 999})
        response = self.client.get(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cdr_list(self):
        url = reverse('cdr-list')
        response = self.client.get(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cdr_delete(self):
        url = reverse('cdr-detail', kwargs={'pk': self.cdr1.pk})
        response = self.client.delete(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update(self):
        url = reverse('cdr-detail', kwargs={'pk': self.cdr1.pk})
        data = {'calling_number': '996704383070',
                'called_number': '996550605073',
                'start_time': '2023-11-22T16:55:59.646000+06:00',
                'end_time': '2023-11-22T16:55:59.646000+06:00',
                'duration': '00:15:00',
                'call_status': CallStatus.unanswered,
                'call_type': CallType.outgoing}
        response = self.client.put(url, data, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        url = reverse('cdr-list')
        data = {'calling_number': '996704383070',
                'called_number': '996550605073',
                'start_time': '2023-11-22T16:55:59.646000+06:00',
                'end_time': '2023-11-22T16:55:59.646000+06:00',
                'duration': '00:15:00',
                'call_status': CallStatus.unanswered,
                'call_type': CallType.outgoing}
        response = self.client.post(url, data, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cdr_filter(self):
        url = reverse('cdr-list')

        response = self.client.get(url, {'call_status': CallStatus.successful,
                                         'start_time': '2023-11-20T16:55:59.646000+06:00',
                                         'end_time': '2023-11-21T16:55:59.646000+06:00',
                                         'calling_number': '996704383070'},
                                   format='json', **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data['results']:
            self.assertIn(('call_id', self.cdr1.call_id), item.items())



