from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from django.urls import reverse_lazy


class StatusesTestCase(TestCase):
    fixtures = ['labels.json', 'statuses.json', 'tasks.json', 'users.json']

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.status3 = Status.objects.get(pk=3)

    def test_read_unauthenticated(self):
        self.client.logout()

        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_read_authenticated(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse_lazy('statuses_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/index.html')

    def test_create_unauthenticated(self):
        self.client.logout()

        response = self.client.get(reverse_lazy('status_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_authenticated(self):
        new_status = {
            'name': 'On Hold',
            'created_at': "2024-09-13 00:00:01.826553+03"
        }

        self.client.force_login(self.user)

        response = self.client.get(reverse_lazy('status_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/create.html')

        response = self.client.post(reverse_lazy('status_create'), new_status)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.get(id=4).name, 'On Hold')
        self.assertRedirects(response, reverse_lazy('statuses_index'))

    def test_update_unauthenticated(self):
        update_url = reverse_lazy('status_update', kwargs={'pk': self.status1.id})

        self.client.logout()

        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_authenticated(self):
        update_url = reverse_lazy('status_update', kwargs={'pk': self.status1.id})

        self.client.force_login(self.user)

        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')

        updated_data = {
            'name': 'Updated',
        }

        response = self.client.post(update_url, updated_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Status.objects.get(pk=1).name, 'Updated')
        self.assertRedirects(response, reverse_lazy('statuses_index'))

    def test_delete_unauthenticated(self):
        delete_url = reverse_lazy('status_delete', kwargs={'pk': self.status3.id})

        self.client.logout()

        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_authenticated(self):
        delete_url = reverse_lazy('status_delete', kwargs={'pk': self.status3.id})

        self.client.force_login(self.user)

        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses_index'))
        self.assertFalse(Status.objects.contains(self.status3))

    def test_delete_linked(self):
        delete_url = reverse_lazy('status_delete', kwargs={'pk': self.status2.id})

        self.client.force_login(self.user)

        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses_index'))
        self.assertTrue(Status.objects.contains(self.status2))
