from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Dog

class DogAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dog_data = {'name': 'Buddy', 'breed': 'Golden Retriever', 'age': 5}
        self.response = self.client.post('/dogs/', self.dog_data, format='json')

    def test_create_dog(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dog.objects.count(), 1)
        self.assertEqual(Dog.objects.get().name, 'Buddy')

    def test_get_dog(self):
        dog = Dog.objects.create(name='Max', breed='Labrador', age=3)
        response = self.client.get(f'/dogs/{dog.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Max')

    def test_update_dog(self):
        dog = Dog.objects.get()
        new_data = {'name': 'Buddy', 'breed': 'Golden Retriever', 'age': 6}
        response = self.client.put(f'/dogs/{dog.id}/', new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['age'], 6)

    def test_delete_dog(self):
        dog = Dog.objects.get()
        response = self.client.delete(f'/dogs/{dog.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dog.objects.count(), 0)
