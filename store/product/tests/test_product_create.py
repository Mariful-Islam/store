from django.test import TestCase
from django.urls import reverse
from rest_framework import status

class TestProductCreate(TestCase):
    def setUp(self):
        self.api_url = reverse('product_api_products_create')
        

    def test_product_create(self):
        product_payload = {
            "name": "Tshirt",
            "description": "This is high quality fabric tshirt",
            "slug": "t-shirt",
            "category": "mens wear"
        }
        response = self.client.post(self.api_url, product_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)